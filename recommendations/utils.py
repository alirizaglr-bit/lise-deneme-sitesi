from collections import Counter
import random

from django.db.models import Q

from exams.models import ExamAttempt, StudentAnswer, Question, Topic


def get_weak_topics(student, limit=5):
    """
    Öğrencinin yanlış yaptığı konuları frekansına göre döndürür.
    """
    wrong_answers = (
        StudentAnswer.objects.filter(
            attempt__student=student,
            is_correct=False,
        )
        .exclude(selected_option__isnull=True)
        .exclude(selected_option='')
    )

    topic_counter = Counter()
    for ans in wrong_answers.select_related('question').prefetch_related('question__topics'):
        for topic in ans.question.topics.all():
            topic_counter[topic.id] += 1

    weak_topic_ids = [tid for tid, _ in topic_counter.most_common(limit)]
    return Topic.objects.filter(id__in=weak_topic_ids)


def get_recommended_questions(student, num_questions=10):
    """
    Öğrencinin zayıf konularından, daha önce çözmediği veya yanlış yaptığı soruları önerir.
    """
    weak_topics = list(get_weak_topics(student, limit=3))

    if not weak_topics:
        return list(Question.objects.order_by('?')[:num_questions])

    questions = Question.objects.filter(topics__in=weak_topics).distinct()

    attempted_question_ids = (
        StudentAnswer.objects.filter(attempt__student=student)
        .values_list('question_id', flat=True)
        .distinct()
    )

    wrong_question_ids = (
        StudentAnswer.objects.filter(attempt__student=student, is_correct=False)
        .values_list('question_id', flat=True)
        .distinct()
    )

    recommended_qs = questions.filter(
        Q(id__in=wrong_question_ids) | ~Q(id__in=attempted_question_ids)
    ).distinct()

    if recommended_qs.count() < num_questions:
        extra = questions.exclude(
            id__in=recommended_qs.values_list('id', flat=True)
        )[: num_questions - recommended_qs.count()]
        recommended = list(recommended_qs) + list(extra)
    else:
        recommended = list(recommended_qs)

    random.shuffle(recommended)
    return recommended[:num_questions]

