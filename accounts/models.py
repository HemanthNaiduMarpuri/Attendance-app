from django.db import models
from django.contrib.auth.models import AbstractUser
from academics.models import Section

ROLE_CHOICES = (
    ('student', 'student'),
    ('admin', 'admin')
)

class User(AbstractUser):
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="register_user_set", 
        related_query_name="register_user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="register_user_permissions_set", 
        related_query_name="register_user",
    )

    def __str__(self):
        return f"{self.username} -> {self.user_role}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    application_number = models.CharField(max_length=20, null=True, blank=True)
    section = models.ForeignKey('academics.Section', on_delete=models.PROTECT, related_name='user_section', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.application_number}"

