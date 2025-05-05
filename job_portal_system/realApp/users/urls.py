from django.urls import path
from .views import dashboard, profile_view

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),  # For normal users
    path('profile/', profile_view, name='profile'),
]