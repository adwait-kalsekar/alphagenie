from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.

class TraderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='user_profiles/', default="user_profiles/default_user.png")
    funds = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_invested = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_returns = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        TraderProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.traderprofile.save()