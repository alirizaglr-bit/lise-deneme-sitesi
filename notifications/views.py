from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Notification


@login_required
def notification_list(request):
    """Kullanıcının tüm bildirimlerini listele."""
    notifications = Notification.objects.filter(recipient=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(
        request,
        'notifications/list.html',
        {
            'notifications': notifications,
            'unread_count': unread_count,
        },
    )


@login_required
def mark_as_read(request, notification_id):
    """Tek bir bildirimi okundu işaretle."""
    notification = get_object_or_404(
        Notification, id=notification_id, recipient=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect('notifications:list')


@login_required
def mark_all_read(request):
    """Tüm bildirimleri okundu işaretle."""
    Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).update(is_read=True)
    return redirect('notifications:list')


@login_required
def get_unread_count(request):
    """AJAX için okunmamış bildirim sayısını döndür."""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).count()
    return JsonResponse({'unread_count': count})


@login_required
def get_recent_notifications(request):
    """Son 5 bildirimi JSON olarak döndür (header dropdown için)."""
    notifications = Notification.objects.filter(recipient=request.user)[:5]
    data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'link': n.link,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%d.%m.%Y %H:%M'),
        }
        for n in notifications
    ]
    return JsonResponse({'notifications': data})

