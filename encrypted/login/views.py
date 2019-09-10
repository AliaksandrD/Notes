from django.shortcuts import render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import generic
from . import forms
# Create your views here.

#User Signup view
class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "login/signup.html"