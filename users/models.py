from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    exp = models.IntegerField(default=0)
    age = models.IntegerField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return self.username

# Automatically create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()