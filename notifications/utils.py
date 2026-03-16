from django.contrib.contenttypes.models import ContentType

from .models import Notification


def create_notification(
    recipient,
    notification_type,
    title,
    message,
    link="",
    sender=None,
    related_object=None,
):
    """
    Yeni bir bildirim oluşturur.
    """
    notification = Notification(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
    )
    if related_object is not None:
        notification.content_type = ContentType.objects.get_for_model(related_object)
        notification.object_id = related_object.pk
    notification.save()
    return notification

