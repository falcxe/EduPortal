from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User
from django import forms


class TeacherApplicationForm(forms.Form):
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'class': 'form-control py-4', 'rows': 5}),
        required=True
    )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Ведите пароль'})
    )
    class Meta:
        model = User
        fields = ('username', 'password')



class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя'})
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'})
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'})
    )
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')