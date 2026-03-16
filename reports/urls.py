from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Öğrenci
    path('ogrenci/', views.student_dashboard, name='student_dashboard'),
    path('ogrenci/sinav/<int:attempt_id>/', views.student_exam_detail, name='student_exam_detail'),

    # Öğretmen
    path('ogretmen/siniflar/', views.teacher_class_list, name='teacher_class_list'),
    path('ogretmen/sinif/<int:class_id>/', views.teacher_class_detail, name='teacher_class_detail'),
    path('ogretmen/rapor/<int:assignment_id>/', views.teacher_class_exam_report, name='teacher_class_exam_report'),
    path('ogretmen/ogrenci/<int:student_id>/', views.teacher_student_detail, name='teacher_student_detail'),

    # Veli
    path('veli/cocuklar/', views.parent_children_list, name='parent_children_list'),
    path('veli/cocuk/<int:child_id>/', views.parent_child_detail, name='parent_child_detail'),
    path('veli/cocuk/<int:child_id>/sinav/<int:attempt_id>/', views.parent_child_exam_detail, name='parent_child_exam_detail'),
]
