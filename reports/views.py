from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Sum, Count
from exams.models import ExamAttempt, Class, Assignment, Exam, Question, StudentAnswer
from accounts.models import User
from django.utils import timezone


# ---------- YARDIMCI DEKORATÖRLER ----------
def teacher_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.user_type == 'teacher', login_url='accounts:login')(view_func)


def parent_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.user_type == 'parent', login_url='accounts:login')(view_func)


# ---------- ÖĞRENCİ RAPORLARI ----------
@login_required
def student_dashboard(request):
    """Öğrenci ana rapor sayfası: genel istatistikler ve son sınavların grafiği"""
    attempts = ExamAttempt.objects.filter(student=request.user, is_finished=True).order_by('-end_time')

    # Genel istatistikler
    total_exams = attempts.count()
    avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    total_correct = attempts.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
    total_wrong = attempts.aggregate(Sum('wrong_count'))['wrong_count__sum'] or 0
    total_empty = attempts.aggregate(Sum('empty_count'))['empty_count__sum'] or 0

    # Son 5 sınav (grafik için)
    last_attempts = attempts[:5]
    dates = [a.end_time.strftime('%d.%m.%Y') for a in last_attempts]
    scores = [float(a.score) for a in last_attempts]

    context = {
        'total_exams': total_exams,
        'avg_score': round(avg_score, 2),
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'total_empty': total_empty,
        'last_attempts': last_attempts,
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'reports/student/dashboard.html', context)


@login_required
def student_exam_detail(request, attempt_id):
    """Belirli bir sınavın soru bazlı detay raporu"""
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user, is_finished=True)
    exam = attempt.exam
    questions = exam.questions.all().order_by('order')

    results = []
    for q in questions:
        ans = attempt.answers.filter(question=q).first()
        results.append({
            'question': q,
            'selected': ans.selected_option if ans else None,
            'correct': q.correct_answer,
            'is_correct': ans.is_correct if ans else False,
        })

    context = {
        'attempt': attempt,
        'exam': exam,
        'results': results,
    }
    return render(request, 'reports/student/exam_detail.html', context)


# ---------- ÖĞRETMEN RAPORLARI ----------
@teacher_required
def teacher_class_list(request):
    """Öğretmenin oluşturduğu sınıfların listesi"""
    classes = Class.objects.filter(teacher=request.user)
    return render(request, 'reports/teacher/class_list.html', {'classes': classes})


@teacher_required
def teacher_class_detail(request, class_id):
    """Sınıf detayı: öğrenci listesi ve genel başarı özeti"""
    cls = get_object_or_404(Class, id=class_id, teacher=request.user)
    students = cls.students.all().order_by('last_name', 'first_name')

    student_stats = []
    for student in students:
        attempts = ExamAttempt.objects.filter(student=student, is_finished=True)
        avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
        total_exams = attempts.count()
        student_stats.append({
            'student': student,
            'avg_score': round(avg_score, 2),
            'total_exams': total_exams,
        })

    # Sınıfa atanmış sınavlar
    assignments = Assignment.objects.filter(assigned_to_class=cls, is_active=True)

    context = {
        'class': cls,
        'student_stats': student_stats,
        'assignments': assignments,
    }
    return render(request, 'reports/teacher/class_detail.html', context)


@teacher_required
def teacher_class_exam_report(request, assignment_id):
    """Belirli bir sınav atamasının sınıf bazlı raporu (hangi öğrenci ne yapmış, en çok yanlış yapılan sorular)"""
    assignment = get_object_or_404(Assignment, id=assignment_id, assigned_to_class__teacher=request.user)
    exam = assignment.exam
    students = assignment.assigned_to_class.students.all() if assignment.assigned_to_class else assignment.assigned_to_students.all()

    student_results = []
    for student in students:
        attempt = ExamAttempt.objects.filter(student=student, exam=exam, is_finished=True).first()
        if attempt:
            student_results.append({
                'student': student,
                'attempt': attempt,
                'score': attempt.score,
                'correct': attempt.correct_count,
                'wrong': attempt.wrong_count,
                'empty': attempt.empty_count,
            })
        else:
            student_results.append({
                'student': student,
                'attempt': None,
                'score': None,
                'correct': None,
                'wrong': None,
                'empty': None,
            })

    # En çok yanlış yapılan sorular (tüm sınıf bazında)
    wrong_questions = {}
    for student in students:
        attempt = ExamAttempt.objects.filter(student=student, exam=exam, is_finished=True).first()
        if attempt:
            wrong_answers = attempt.answers.filter(is_correct=False).exclude(selected_option__isnull=True).exclude(selected_option='')
            for ans in wrong_answers:
                qid = ans.question.id
                wrong_questions[qid] = wrong_questions.get(qid, 0) + 1
    sorted_wrong = sorted(wrong_questions.items(), key=lambda x: x[1], reverse=True)[:10]
    top_wrong_questions = []
    for qid, count in sorted_wrong:
        q = Question.objects.get(id=qid)
        top_wrong_questions.append({'question': q, 'wrong_count': count})

    context = {
        'assignment': assignment,
        'exam': exam,
        'student_results': student_results,
        'top_wrong_questions': top_wrong_questions,
    }
    return render(request, 'reports/teacher/exam_report.html', context)


@teacher_required
def teacher_student_detail(request, student_id):
    """Öğretmenin sınıfındaki bir öğrencinin tüm sınav performansı"""
    teacher_classes = Class.objects.filter(teacher=request.user)
    student = get_object_or_404(User, id=student_id, user_type='student', enrolled_classes__in=teacher_classes)
    attempts = ExamAttempt.objects.filter(student=student, is_finished=True).order_by('-end_time')

    total_exams = attempts.count()
    avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    total_correct = attempts.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
    total_wrong = attempts.aggregate(Sum('wrong_count'))['wrong_count__sum'] or 0
    total_empty = attempts.aggregate(Sum('empty_count'))['empty_count__sum'] or 0

    # Son 5 sınav grafiği
    last_attempts = attempts[:5]
    dates = [a.end_time.strftime('%d.%m.%Y') for a in last_attempts]
    scores = [float(a.score) for a in last_attempts]

    context = {
        'student': student,
        'total_exams': total_exams,
        'avg_score': round(avg_score, 2),
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'total_empty': total_empty,
        'last_attempts': last_attempts,
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'reports/teacher/student_detail.html', context)


# ---------- VELİ RAPORLARI ----------
@parent_required
def parent_children_list(request):
    """Velilerin kayıtlı çocuklarının listesi"""
    children = request.user.children.all()
    return render(request, 'reports/parent/children_list.html', {'children': children})


@parent_required
def parent_child_detail(request, child_id):
    """Velinin seçtiği çocuğun performans raporu (öğrenci dashboard'una benzer)"""
    child = get_object_or_404(User, id=child_id, parent=request.user, user_type='student')
    attempts = ExamAttempt.objects.filter(student=child, is_finished=True).order_by('-end_time')

    total_exams = attempts.count()
    avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    total_correct = attempts.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
    total_wrong = attempts.aggregate(Sum('wrong_count'))['wrong_count__sum'] or 0
    total_empty = attempts.aggregate(Sum('empty_count'))['empty_count__sum'] or 0

    last_attempts = attempts[:5]
    dates = [a.end_time.strftime('%d.%m.%Y') for a in last_attempts]
    scores = [float(a.score) for a in last_attempts]

    context = {
        'child': child,
        'total_exams': total_exams,
        'avg_score': round(avg_score, 2),
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'total_empty': total_empty,
        'last_attempts': last_attempts,
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'reports/parent/child_detail.html', context)


@parent_required
def parent_child_exam_detail(request, child_id, attempt_id):
    """Velinin çocuğunun belirli bir sınav detayı"""
    child = get_object_or_404(User, id=child_id, parent=request.user, user_type='student')
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=child, is_finished=True)
    exam = attempt.exam
    questions = exam.questions.all().order_by('order')

    results = []
    for q in questions:
        ans = attempt.answers.filter(question=q).first()
        results.append({
            'question': q,
            'selected': ans.selected_option if ans else None,
            'correct': q.correct_answer,
            'is_correct': ans.is_correct if ans else False,
        })

    context = {
        'child': child,
        'attempt': attempt,
        'exam': exam,
        'results': results,
    }
    return render(request, 'reports/parent/child_exam_detail.html', context)
