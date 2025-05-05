from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from MainApp.models import Job, SavedJobs, JobApplication
from MainApp.views import login_user
from django.contrib import messages
import requests



def profile_view(request):
    return render(request, 'users/profile.html')



def dashboard(request):
    recipes = Recipe.objects.all()
    return render(request, 'users/dashboard.html', {'recipes': recipes})
