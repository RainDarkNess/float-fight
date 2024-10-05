# myapp/forms.py
from django import forms
from .models import Users, restartCode
from .models import Session
from .models import Article


class RegistrationForm(forms.ModelForm):
    Логин = forms.CharField(max_length=30, label='Логин')
    Пароль = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    Подтверждение_пароля = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')
    Email = forms.EmailField(max_length=30)

    class Meta:
        model = Users
        fields = ['Логин', 'Пароль', 'Подтверждение_пароля']

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("Логин")
        password = cleaned_data.get("Пароль")
        confirm_password = cleaned_data.get("Подтверждение_пароля")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")


class LoginForm(forms.Form):
    Логин = forms.CharField(max_length=30)
    Пароль = forms.CharField(widget=forms.PasswordInput())


class SessionForm(forms.ModelForm):
    Имя_сессии = forms.CharField(max_length=30)
    Имя_игрока = forms.CharField(max_length=30)

    class Meta:
        model = Session
        fields = ['Имя_сессии', 'Имя_игрока']


class RestoreForm(forms.ModelForm):
    Email = forms.EmailField(max_length=30)

    class Meta:
        model = restartCode
        fields = ['Email']


class codeCheck(forms.Form):
    Код_подтверждения = forms.CharField(max_length=4)


class EditPasswordForm(forms.Form):
    Пароль = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    Подтверждение_пароля = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')

    class Meta:
        model = Users
        fields = ['Пароль', 'Подтверждение_пароля']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("Пароль")
        confirm_password = cleaned_data.get("Подтверждение_пароля")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")


class ArticleAdd(forms.Form):
    Название_статьи = forms.CharField(max_length=30)
    Содержание = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))

    # class Meta:
    #     model = Article
    #     fields = ['Название_статьи', 'Содержание', 'Дата_публикации']


class SessionSet(forms.Form):
    Имя_сессии = forms.CharField(max_length=30)
    Имя_игрока = forms.CharField(max_length=30)
