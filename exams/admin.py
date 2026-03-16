from django.contrib import admin
from .models import Exam, Question, ExamAttempt, StudentAnswer, Class, Assignment


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'total_questions', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'exam', 'order', 'correct_answer']
    list_filter = ['exam']
    search_fields = ['text']


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'start_time', 'is_finished', 'score']
    list_filter = ['is_finished', 'exam']


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_option', 'is_correct']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'created_at']
    list_filter = ['teacher']
    search_fields = ['name']
    filter_horizontal = ['students']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['exam', 'assigned_to_class', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'exam']
    filter_horizontal = ['assigned_to_students']
    date_hierarchy = 'start_date'
