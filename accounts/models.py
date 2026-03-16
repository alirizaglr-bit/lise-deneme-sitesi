from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Öğrenci'),
        ('teacher', 'Öğretmen'),
        ('parent', 'Veli'),
        ('admin', 'Yönetici'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        limit_choices_to={'user_type': 'parent'},
        verbose_name='Veli',
    )

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.get_full_name() or self.username
