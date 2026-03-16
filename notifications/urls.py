from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('okundu/<int:notification_id>/', views.mark_as_read, name='mark_read'),
    path('tumunu-okundu-isaretle/', views.mark_all_read, name='mark_all_read'),
    path('ajax/sayac/', views.get_unread_count, name='unread_count'),
    path('ajax/son-bildirimler/', views.get_recent_notifications, name='recent'),
]

