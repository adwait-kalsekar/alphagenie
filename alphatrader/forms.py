from django import forms
from .models import TraderProfile

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = TraderProfile
        fields = ['profile_image']