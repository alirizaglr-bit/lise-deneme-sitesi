from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('exam_assigned', 'Sınav Atandı'),
        ('exam_finished', 'Sınav Tamamlandı'),
        ('exam_reminder', 'Sınav Hatırlatması'),
        ('system', 'Sistem Bildirimi'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Alıcı',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sent_notifications',
        verbose_name='Gönderen',
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='Bildirim Tipi',
    )
    title = models.CharField(max_length=255, verbose_name='Başlık')
    message = models.TextField(verbose_name='Mesaj')
    link = models.CharField(max_length=500, blank=True, verbose_name='Bağlantı')
    is_read = models.BooleanField(default=False, verbose_name='Okundu mu?')
    created_at = models.DateTimeField(auto_now_add=True)

    # İsteğe bağlı: İlgili nesne (örn. ExamAttempt) için generic foreign key
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bildirim'
        verbose_name_plural = 'Bildirimler'

    def __str__(self):
        return f'{self.recipient} - {self.title}'

