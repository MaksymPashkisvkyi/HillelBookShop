import json
import logging
from decimal import Decimal

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from payments.models import Payment
from payments.stripe_service import StripePaymentService
from payments.serializers import PaymentSerializer, CreatePaymentSerializer
from shop.orders.models import Order
from payments.utils import send_receipt

logger = logging.getLogger(__name__)

STRIPE_P_KEY = settings.STRIPE_PUBLIC_KEY
render_async = sync_to_async(render, thread_sensitive=True)


async def checkout_view(request, order_id=None):
    """Render the checkout page and load the requested order asynchronously."""
    order = None
    if order_id:
        try:
            order = await Order.objects.select_related('payment', 'customer').aget(id=order_id)
        except Order.DoesNotExist as exc:
            raise Http404('Order not found') from exc
    return await render_async(request, 'payments/payments/page-checkout.html', {
        'stripe_public_key': STRIPE_P_KEY,
        'order': order,
    })


class PaymentViewSet(viewsets.ModelViewSet):
    """Expose payment CRUD endpoints plus Stripe intent creation and confirmation."""

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Limit payments to the authenticated user."""
        return Payment.objects.filter(user=self.request.user).select_related('user')

    def get_serializer_class(self):
        """Return the serializer required for the current action."""
        if self.action == 'create_payment_intent':
            return CreatePaymentSerializer
        return PaymentSerializer

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        """Create a Stripe payment intent and persist the local payment record."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payment, payment_intent = StripePaymentService.create_payment_intent(
                user=request.user,
                amount=Decimal(serializer.validated_data['amount']),
                currency=serializer.validated_data['currency'],
                description=serializer.validated_data['description'],
                metadata=serializer.validated_data.get('metadata', {}),
            )
            return Response({
                'payment_id': str(payment.id),
                'client_secret': payment_intent.client_secret,
                'amount': str(payment.amount),
                'currency': payment.currency,
                'status': payment.status,
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({
                'error': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error on payment intent creation: {str(e)}')
            return Response({
                'error': _('Failed to create payment intent: %(error)s') % {'error': str(e)},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a payment, link it to an order, and send the receipt email."""
        payment = self.get_object()
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({
                'error': _('order_id is required'),
            }, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id, customer__user=request.user)
        order.payment = payment
        order.save(update_fields=['payment'])

        try:
            payment = StripePaymentService.confirm_payment(
                payment_id=str(payment.id),
                stripe_payment_intent_id=payment.stripe_payment_intent_id
            )
            serializer = self.get_serializer(payment)
            try:
                send_receipt(order)
            except Exception as e:
                logger.warning(f'Payment confirmed, but receipt sending failed: {str(e)}')
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Error on payment intent confirmation: {str(e)}')
            return Response({
                'error': _('Failed to confirm payment intent: %(error)s') % {'error': str(e)},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
