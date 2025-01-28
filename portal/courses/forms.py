from django import forms
from .models import Course, CourseMaterial
from django.core.exceptions import ValidationError
from .models import Comment

class CourseForm(forms.ModelForm):
    class Meta:

        model = Course
        fields = ['name', 'description', 'image', 'grade', 'subject', 'full_text', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),
            'image': forms.FileInput(attrs={  # Меняем ClearableFileInput на FileInput
                'class': 'form-control',
                'accept': 'image/*'  # Добавляем ограничение на типы файлов
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            'full_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите полный текст курса'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите тэги через запятую'
            })
        }

class CourseMaterialForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = CourseMaterial
        fields = ['file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст комментария', 'label': 'Комментарий'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Введите оценку от 1 до 5', 'label': 'Оценка'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ответ',
                'rows': '3'
            })
        }