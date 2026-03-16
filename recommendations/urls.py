from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommended_questions, name='list'),
]

