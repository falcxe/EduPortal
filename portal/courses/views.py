from django.db import models  # Добавьте этот импорт
from .models import Course, CourseMaterial, Comment
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import zipfile
import os
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CourseForm, CourseMaterialForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.views import View


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail_view.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(course=self.object, parent__isnull=True)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = self.object
            comment.user = request.user
            comment.save()
            return redirect('course-detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()

            # Обработка файлов материалов
            files = request.FILES.getlist('materials')
            for file in files:
                CourseMaterial.objects.create(course=course, file=file)

            # Обработка теста, если он был добавлен
            if request.POST.get('has_test'):
                test = Test.objects.create(
                    course=course,
                    title=request.POST.get('test_title')
                )

                # Обработка вопросов и ответов
                questions_data = {}
                for key, value in request.POST.items():
                    if key.startswith('question_'):
                        question_id = key.split('_')[1]
                        if question_id not in questions_data:
                            questions_data[question_id] = {'text': value, 'answers': []}

                    elif key.startswith('answer_'):
                        _, question_id, answer_id = key.split('_')
                        correct = request.POST.get(f'correct_{question_id}') == answer_id
                        questions_data[question_id]['answers'].append({
                            'text': value,
                            'is_correct': correct
                        })

                # Сохранение вопросов и ответов
                for q_data in questions_data.values():
                    question = Question.objects.create(
                        test=test,
                        text=q_data['text']
                    )
                    for a_data in q_data['answers']:
                        Answer.objects.create(
                            question=question,
                            text=a_data['text'],
                            is_correct=a_data['is_correct']
                        )

            return redirect('course-detail', pk=course.pk)  # Изменено с 'catalog' на 'course-detail'
    else:
        form = CourseForm()

    return render(request, 'courses/create.html', {'form': form})


def catalog(request):
    courses = Course.objects.all()
    grade = request.GET.get('grade')
    subject = request.GET.get('subject')
    tags = request.GET.get('tags')

    if grade:
        courses = courses.filter(grade=grade)
    if subject:
        courses = courses.filter(subject=subject)
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            courses = courses.filter(tags__icontains=tag.strip())

    paginator = Paginator(courses, 15)  # Показывать 10 курсов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'selected_grade': grade,
        'selected_subject': subject,
        'selected_tags': tags
    }

    return render(request, 'courses/catalog.html', context)

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create.html'
    context_object_name = 'course'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.object.pk})

def download_all_materials(request, pk):
    course = get_object_or_404(Course, pk=pk)
    materials = course.materials.all()
    zip_filename = f"{course.name}_materials.zip"
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zip_file:
        for material in materials:
            zip_file.write(material.file.path, os.path.basename(material.file.path))

    return response

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            for file in request.FILES.getlist('materials'):
                CourseMaterial.objects.create(course=course, file=file)
            return redirect(course.get_absolute_url())
    else:
        form = CourseForm()
    return render(request, 'courses/create.html', {'form': form})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    comments = Comment.objects.filter(course=course, parent__isnull=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.course = course
            comment.save()
            return redirect('course-detail', pk=course.id)
    else:
        form = CommentForm()
    return render(request, 'courses/detail_view.html', {'course': course, 'comments': comments, 'form': form})

def download_all_materials(request, pk):
    course = get_object_or_404(Course, pk=pk)
    materials = course.materials.all()
    zip_filename = f"{course.name}_materials.zip"
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zip_file:
        for material in materials:
            zip_file.write(material.file.path, os.path.basename(material.file.path))

    return response

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/delete.html'
    success_url = reverse_lazy('catalog')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(author=self.request.user)

class DeleteCommentView(View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if request.user.is_staff or request.user == comment.course.author:
            comment.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=403)

@login_required
def add_reply(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        reply = Comment.objects.create(
            user=request.user,
            course=parent_comment.course,
            parent=parent_comment,
            text=request.POST.get('text')
        )
        return redirect('course-detail', pk=parent_comment.course.pk)

@login_required
def create_test(request, course_id):
    if request.method == 'POST':
        test = Test.objects.create(
            course_id=course_id,
            title=request.POST.get('test_title')
        )

        # Обработка вопросов и ответов
        questions_data = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                if question_id not in questions_data:
                    questions_data[question_id] = {'text': value, 'answers': []}

            elif key.startswith('answer_'):
                parts = key.split('_')
                if len(parts) == 3:
                    _, question_id, answer_id = parts
                    correct = request.POST.get(f'correct_answer_{question_id}') == answer_id
                    questions_data[question_id]['answers'].append({
                        'text': value,
                        'is_correct': correct
                    })

        # Сохранение вопросов и ответов
        for q_data in questions_data.values():
            question = Question.objects.create(
                test=test,
                text=q_data['text']
            )
            for a_data in q_data['answers']:
                Answer.objects.create(
                    question=question,
                    text=a_data['text'],
                    is_correct=a_data['is_correct']
                )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)