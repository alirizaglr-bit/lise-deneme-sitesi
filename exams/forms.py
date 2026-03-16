from django import forms
from .models import Exam, Question, Assignment, Class


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'duration', 'total_questions', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'correct_answer', 'explanation', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 2}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assigned_to_class', 'assigned_to_students', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'assigned_to_students': forms.SelectMultiple(attrs={'size': 10}),
        }

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        self.exam = kwargs.pop('exam', None)
        super().__init__(*args, **kwargs)
        if self.teacher:
            self.fields['assigned_to_class'].queryset = Class.objects.filter(teacher=self.teacher)


class BulkQuestionUploadForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exam.objects.none(), label="Sınav Seçin")
    file = forms.FileField(
        label="Excel/CSV Dosyası",
        help_text=(
            "Dosya formatı: Soru metni, A şıkkı, B şıkkı, C şıkkı, D şıkkı, "
            "E şıkkı (opsiyonel), Doğru cevap (A,B,C,D,E), Açıklama (opsiyonel), "
            "Sıra (opsiyonel)"
        ),
    )

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields["exam"].queryset = Exam.objects.filter(created_by=teacher)
