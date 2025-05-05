from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default-profile.jpg')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default = 'user')
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    # Fixing clashes by setting unique related_names
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.username
    
    def is_admin(self):
        return self.user_type == 'admin'
    
    def is_normal_user(self):
        return self.user_type == 'user'
