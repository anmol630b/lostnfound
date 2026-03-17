from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone           = models.CharField(max_length=15, blank=True)
    city            = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio             = models.TextField(blank=True)
    is_verified     = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_avatar_text(self):
        name = self.user.get_full_name() or self.user.username
        return name[0].upper()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
