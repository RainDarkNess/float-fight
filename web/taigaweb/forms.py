# myapp/forms.py
from django import forms
from .models import Users
from .models import Session


class RegistrationForm(forms.ModelForm):
    login = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm password')

    class Meta:
        model = Users
        fields = ['login', 'password']

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")


class LoginForm(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class SessionForm(forms.ModelForm):
    Имя_сессии = forms.CharField(max_length=30)
    Имя_игрока = forms.CharField(max_length=30)

    class Meta:
        model = Session
        fields = ['Имя_сессии', 'Имя_игрока']


class SessionSet(forms.Form):
    Имя_сессии = forms.CharField(max_length=30)
    Имя_игрока = forms.CharField(max_length=30)

