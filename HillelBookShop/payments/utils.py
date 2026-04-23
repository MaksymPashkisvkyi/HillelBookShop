from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_receipt(email, order):
    # send_mail(
    #     subject="Hillel Book Shop",
    #     message=f"Hillel Book Shop <{email}>",
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[email],
    # )
    html_content = render_to_string('payments/email/order_receipt.html', {'order': order})
    email = EmailMultiAlternatives(
        subject=f'Замовлення #{order.id}',
        from_email=None,
        to=[order.email],
    )
    email.attach_alternative(html_content, mimetype='text/html')
    email.send()
