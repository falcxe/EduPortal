from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.conf import settings


class Course(models.Model):
    GRADE_CHOICES = [(i, str(i)) for i in range(1, 12)]
    SUBJECT_CHOICES = sorted([
        ('Алгебра', 'Алгебра'),
        ('Английский язык', 'Английский язык'),
        ('Биология', 'Биология'),
        ('География', 'География'),
        ('Геометрия', 'Геометрия'),
        ('История', 'История'),
        ('Информатика', 'Информатика'),
        ('Литература', 'Литература'),
        ('Математика', 'Математика'),
        ('Обществознание', 'Обществознание'),
        ('Русский язык', 'Русский язык'),
        ('Физика', 'Физика'),
        ('Химия', 'Химия'),
    ], key=lambda x: x[0])

    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.CharField(max_length=200, verbose_name="Описание")
    image = models.ImageField(upload_to='courses_images/', verbose_name='Изображение курса', null=True, help_text="Загрузите изображение для курса")
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name="Класс")
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES, verbose_name="Предмет")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
    full_text = models.TextField(help_text="Полный текст курса", verbose_name="Полный текст")
    tags = models.CharField(max_length=200, verbose_name="Тэги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})
    @property
    def average_rating(self):
        ratings = Comment.objects.filter(course=self, rating__isnull=False).values_list('rating', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings), 1)
        return 0.0

    @property
    def rating_count(self):
        return Comment.objects.filter(course=self, rating__isnull=False).count()

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_materials/', blank=False, verbose_name="Файл")

    def __str__(self):
        return self.file.name


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField(verbose_name="Текст комментария")
    rating = models.PositiveIntegerField(null=True, blank=True, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.course.name}'
