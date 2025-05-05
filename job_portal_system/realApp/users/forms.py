from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','user_type', 'profile_picture', 'bio', 'phone_number', 'address', 'date_of_birth']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'bio', 'phone_number', 'address', 'date_of_birth']