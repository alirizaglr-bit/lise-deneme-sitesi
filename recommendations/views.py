from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .utils import get_recommended_questions


@login_required
def recommended_questions(request):
    """Öğrenciye önerilen soruları listele."""
    if getattr(request.user, 'user_type', None) != 'student':
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")

    questions = get_recommended_questions(request.user, num_questions=15)
    return render(request, 'recommendations/list.html', {'questions': questions})

