from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Student, User
from django.views import generic
from .forms import StudentCreationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView


class SignUpView(generic.CreateView):
    model = User
    form_class = StudentCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Registered Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Registration UnSuccessful")
        return super().form_invalid(form)
 
class StudentLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    