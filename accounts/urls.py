from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('giris/', views.CustomLoginView.as_view(), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('kayit/', views.register, name='register'),
    path('profil/', views.profile, name='profile'),
    path('sifre-degistir/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             success_url=reverse_lazy('accounts:password_change_done')
         ), name='password_change'),
    path('sifre-degistir/tamam/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ), name='password_change_done'),
]
