from django.db import models
from django.conf import settings


class Topic(models.Model):
    name = models.CharField(max_length=100, verbose_name="Konu Adı")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtopics',
        verbose_name="Üst Konu",
    )
    description = models.TextField(blank=True, verbose_name="Açıklama")

    class Meta:
        verbose_name = "Konu"
        verbose_name_plural = "Konular"

    def __str__(self):
        return self.name


class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sınav Başlığı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    duration = models.IntegerField(help_text="Dakika cinsinden", verbose_name="Süre")
    total_questions = models.IntegerField(verbose_name="Soru Sayısı")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Oluşturan")

    class Meta:
        verbose_name = "Sınav"
        verbose_name_plural = "Sınavlar"

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name="Sınav")
    text = models.TextField(verbose_name="Soru Metni")
    image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Soru Görseli")
    option_a = models.CharField(max_length=255, verbose_name="A Şıkkı")
    option_b = models.CharField(max_length=255, verbose_name="B Şıkkı")
    option_c = models.CharField(max_length=255, verbose_name="C Şıkkı")
    option_d = models.CharField(max_length=255, verbose_name="D Şıkkı")
    option_e = models.CharField(max_length=255, blank=True, null=True, verbose_name="E Şıkkı (opsiyonel)")
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')],
        verbose_name="Doğru Cevap"
    )
    explanation = models.TextField(blank=True, help_text="Video çözüm linki veya açıklama", verbose_name="Çözüm Açıklaması")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    topics = models.ManyToManyField(
        Topic,
        related_name='questions',
        blank=True,
        verbose_name="Konular",
    )

    class Meta:
        verbose_name = "Soru"
        verbose_name_plural = "Sorular"
        ordering = ['order']

    def __str__(self):
        return f"{self.exam.title} - Soru {self.order}"


class ExamAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts', verbose_name="Öğrenci")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts', verbose_name="Sınav")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True, verbose_name="Puan")
    correct_count = models.IntegerField(default=0)
    wrong_count = models.IntegerField(default=0)
    empty_count = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sınav Girişimi"
        verbose_name_plural = "Sınav Girişimleri"

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"


class StudentAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)  # A,B,C,D,E veya boş
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Öğrenci Cevabı"
        verbose_name_plural = "Öğrenci Cevapları"
        unique_together = [['attempt', 'question']]

    def __str__(self):
        return f"{self.attempt.student.username} - Soru {self.question.id}"


class Class(models.Model):
    name = models.CharField(max_length=100, verbose_name="Sınıf Adı")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classes',
        verbose_name="Öğretmen",
        limit_choices_to={'user_type': 'teacher'}
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_classes',
        verbose_name="Öğrenciler",
        limit_choices_to={'user_type': 'student'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sınıf"
        verbose_name_plural = "Sınıflar"

    def __str__(self):
        return f"{self.name} - {self.teacher.get_full_name()}"


class Assignment(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='assignments', verbose_name="Sınav")
    assigned_to_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assignments',
        verbose_name="Atanan Sınıf"
    )
    assigned_to_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='assigned_exams',
        verbose_name="Atanan Öğrenciler",
        limit_choices_to={'user_type': 'student'}
    )
    start_date = models.DateTimeField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateTimeField(verbose_name="Bitiş Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Sınav Atama"
        verbose_name_plural = "Sınav Atamaları"

    def __str__(self):
        return f"{self.exam.title} ataması"
