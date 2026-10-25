from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['is_young_specialist', 'university', 'course', 'skills', 'role_in_mc']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'role_in_mc': forms.Select(attrs={'class': 'form-select'}),
        }
