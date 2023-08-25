from django import forms
from django.contrib.auth.forms import UserCreationForm
from project.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

# class RegistrationForm(forms.Form):
#     email = forms.EmailField(label='Почта')
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#     full_name = forms.CharField(label='ФИО')

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         return email

#     def clean_password(self):
#         password = self.cleaned_data['password']
#         return password

#     def clean_full_name(self):
#         full_name = self.cleaned_data['full_name']
#         return full_name
