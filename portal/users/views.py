from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import UserLoginForm, UserRegisterForm, TeacherApplicationForm
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_teacher(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_staff:
        user.is_teacher = True
        user.save()
        messages.success(request, f'Пользователь {user.username} теперь учитель.')
    else:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
    return redirect('admin:index')

@login_required
@user_passes_test(lambda u: u.is_staff)
def reject_teacher(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_staff:
        messages.success(request, f'Заявка пользователя {user.username} отклонена.')
    else:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
    return redirect('admin:index')

def apply_for_teacher(request):
    if request.method == 'POST':
        form = TeacherApplicationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            subject = "Кто-то подал заявку на преподавание"

            # Ссылка на админ панель
            admin_url = request.build_absolute_uri(reverse('admin:index'))

            email_message = f"""
            Пользователь: {request.user.username} хочет стать преподавателем.
            Сообщение: {message}
            <br><br>
            <a href="{admin_url}">Перейти в админ панель</a>
            """
            plain_message = strip_tags(email_message)

            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message=email_message, fail_silently=False)
            messages.success(request, 'Ваша заявка на преподавание отправлена. Ожидайте подтверждения')
            return redirect('profile')
    else:
        form = TeacherApplicationForm()
    return render(request, 'users/apply_for_teacher.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)

def profile(request):
    form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/profile.html', context)

def reset_password(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы должны быть авторизованы, чтобы изменить пароль')
        return redirect('login')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            try:
                validate_password(new_password, request.user)
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Пароль успешно изменен')
                return redirect('profile')
            except ValidationError as e:
                messages.error(request, e)
        else:
            messages.error(request, 'Пароли не совпадают')

    return render(request, 'users/reset_password.html')

def logout(request):
    auth.logout(request)
    return redirect('index')


def auth_error(request):
    error_message = request.session.pop('social_auth_error', None)
    return render(request, 'users/auth_error.html', {'error': error_message})
