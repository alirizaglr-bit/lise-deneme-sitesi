from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exams.models import ExamAttempt, Exam, Assignment, Class
from accounts.models import User
from django.db.models import Avg, Sum, Count
from django.utils import timezone


@login_required
def home(request):
    user = request.user
    context = {}

    if user.user_type == 'student':
        attempts = ExamAttempt.objects.filter(student=user, is_finished=True).order_by('-end_time')[:5]
        enrolled_classes = user.enrolled_classes.all()
        assignments_qs = Assignment.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            assigned_to_class__in=enrolled_classes,
        ) | Assignment.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            assigned_to_students=user,
        )

        pending_exams = []
        for assignment in assignments_qs.distinct():
            attempt = ExamAttempt.objects.filter(
                student=user,
                exam=assignment.exam,
                is_finished=False,
            ).first()
            if not attempt:
                pending_exams.append(assignment.exam)

        context['recent_attempts'] = attempts
        context['pending_exams'] = pending_exams[:5]

    elif user.user_type == 'teacher':
        classes = Class.objects.filter(teacher=user)
        class_stats = []
        for cls in classes:
            student_count = cls.students.count()
            active_assignments = Assignment.objects.filter(
                assigned_to_class=cls,
                is_active=True,
                end_date__gte=timezone.now(),
            ).count()
            class_stats.append({
                'class': cls,
                'student_count': student_count,
                'active_assignments': active_assignments,
            })
        context['class_stats'] = class_stats
        recent_exams = Exam.objects.filter(created_by=user).order_by('-created_at')[:5]
        context['recent_exams'] = recent_exams

    elif user.user_type == 'parent':
        children = user.children.all()
        children_stats = []
        for child in children:
            attempts = ExamAttempt.objects.filter(student=child, is_finished=True)
            avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
            total_exams = attempts.count()
            last_attempt = attempts.order_by('-end_time').first()
            children_stats.append({
                'child': child,
                'avg_score': round(avg_score, 2),
                'total_exams': total_exams,
                'last_attempt': last_attempt,
            })
        context['children_stats'] = children_stats

    return render(request, 'dashboard/home.html', context)
