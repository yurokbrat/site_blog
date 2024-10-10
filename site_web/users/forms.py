from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = forms.CharField(
        label="Логин пользователя", help_text="Только буквы, цифры и @/./+/-/_"
    )
    email = forms.EmailField(label="Адрес электронной почты")
    password1 = forms.CharField(
        label="Пароль",
        help_text="Ваш пароль не должен быть похож на другую вашу персональную информацию, "
        "должен содержать как минимум 8 символов, не может быть общеиспользуемым "
        "паролем и не может состоять только из цифр.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        help_text="Введите тот же самый пароль для проверки.",
    )

    error_messages = {
        "password_mismatch": "Пароли не совпадают.",
        "username_exists": "Пользователь с таким именем уже существует.",
        "invalid_username": "Недопустимое имя пользователя. Используйте только буквы, цифры и символы @/./+/-/_",
        "password_too_common": "Слишком лёгкий пароль. Выберите более сложный пароль.",
        "password_numeric_only": "Пароль не может состоять только из цифр.",
        "password_too_short": "Пароль слишком короткий. Минимальная длина - 8 символов.",
        "password_too_long": "Пароль слишком длинный. Максимальная длина - 150 символов.",
        "invalid_email": "Некорректный адрес электронной почты.",
        "email_exists": "Пользователь с таким адресом электронной почты уже существует.",
    }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

    username = forms.CharField(
        label="Логин пользователя", help_text="Только буквы, цифры и @/./+/-/_"
    )
    email = forms.EmailField(label="Адрес электронной почты")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
        labels = {"image": "Фото профиля"}
