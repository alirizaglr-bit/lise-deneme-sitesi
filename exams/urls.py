from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='list'),
    path('<int:exam_id>/', views.exam_detail, name='detail'),
    path('<int:exam_id>/basla/', views.start_exam, name='start'),
    path('sinav/<int:attempt_id>/', views.take_exam, name='take_exam'),
    path('sinav/<int:attempt_id>/kaydet/', views.save_answer, name='save_answer'),
    path('sinav/<int:attempt_id>/bitir/', views.finish_exam, name='finish_exam'),
    path('sonuc/<int:attempt_id>/', views.exam_result, name='exam_result'),
    # Öğretmen paneli URL'leri
    path('ogretmen/sinavlar/', views.teacher_exam_list, name='teacher_exam_list'),
    path('ogretmen/sinav/ekle/', views.teacher_exam_create, name='teacher_exam_create'),
    path('ogretmen/siniflar/', views.teacher_class_list, name='teacher_class_list'),
    path('ogretmen/sinif/ekle/', views.teacher_class_create, name='teacher_class_create'),
    path('ogretmen/sinif/<int:class_id>/', views.teacher_class_manage, name='teacher_class_manage'),
    path('ogretmen/sinif/<int:class_id>/cikar/<int:student_id>/', views.teacher_class_remove_student, name='teacher_class_remove_student'),
    path('ogretmen/sinav/<int:exam_id>/duzenle/', views.teacher_exam_edit, name='teacher_exam_edit'),
    path('ogretmen/sinav/<int:exam_id>/sil/', views.teacher_exam_delete, name='teacher_exam_delete'),
    path('ogretmen/sinav/<int:exam_id>/ata/', views.teacher_assign_exam, name='teacher_assign_exam'),
    path('ogretmen/sinav/<int:exam_id>/toplu-yukle/', views.teacher_bulk_upload, name='teacher_bulk_upload'),
    path('ogretmen/soru/toplu-yukle/', views.teacher_bulk_question_upload, name='teacher_bulk_question_upload'),
    path('ogretmen/sinav/<int:exam_id>/sorular/', views.teacher_question_list, name='teacher_question_list'),
    path('ogretmen/sinav/<int:exam_id>/soru/ekle/', views.teacher_question_create, name='teacher_question_create'),
    path('ogretmen/soru/<int:question_id>/duzenle/', views.teacher_question_edit, name='teacher_question_edit'),
    path('ogretmen/soru/<int:question_id>/sil/', views.teacher_question_delete, name='teacher_question_delete'),
]
