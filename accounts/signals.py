from django.db.models.signals import post_save
from .models import Student, User
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_role == 'student':
            Student.objects.get_or_create(user=instance)