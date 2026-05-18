from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def send_receipt(order):
    html_content = render_to_string('payments/email/order_receipt.html', {'order': order})
    email = EmailMultiAlternatives(
        subject=_('Order #%(order_id)s') % {'order_id': order.id},
        from_email=None,
        to=[order.email],
    )
    email.attach_alternative(html_content, mimetype='text/html')
    email.send()
