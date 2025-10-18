from django import forms
from dashboard.models import Service
from django import forms
from datetime import timedelta
from booking.models import Staff

class ServiceForm(forms.ModelForm):
    
    duration_minutes = forms.IntegerField(
        min_value=0,
        label="Duration (minutes)",
        help_text="Enter duration in minutes"
    )

    class Meta:
        model = Service
        fields = ['name', 'description', 'image', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        minutes = self.cleaned_data['duration_minutes']
        instance.duration = timedelta(minutes=minutes)
        if commit:
            instance.save()
        return instance


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'name', 'is_active']
