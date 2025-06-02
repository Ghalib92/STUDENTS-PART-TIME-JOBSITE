from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control custom-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control custom-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control custom-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control custom-input'}))
