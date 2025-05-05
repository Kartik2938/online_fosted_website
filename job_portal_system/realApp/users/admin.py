from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'profile_picture']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'bio')}),('Additional Info', {'fields':('user_type',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)