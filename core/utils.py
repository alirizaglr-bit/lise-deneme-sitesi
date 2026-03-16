from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification_email(subject, template_name, context, recipient_list):
    """
    Genel e-posta gönderme fonksiyonu.

    template_name: 'emails/...' şeklinde bir şablon adı
    context: şablona gönderilecek değişkenler
    recipient_list: ['email@example.com'] listesi
    """
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

