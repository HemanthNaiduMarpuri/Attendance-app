from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Student
from academics.models import Section
from django.contrib.auth.forms import AuthenticationForm

class StudentCreationForm(UserCreationForm):
    application_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Application Number'}))
    email = forms.EmailField(max_length=96, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=True,
        widget=forms.RadioSelect
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "application_number",
            "password1",
            "password2",
            "section",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({
                    "class": "form-control",
                    "style": "width:100%;"
                })

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError("Email Already Exists")
        return email

    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_role = 'student'
        user.save()

        student = user.user_profile
        student.application_number = self.cleaned_data['application_number']
        student.section = self.cleaned_data['section']
        student.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Username",
        })
        self.fields['password'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
        })