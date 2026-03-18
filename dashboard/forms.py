from django import forms
from .models import SymptomUpdate

class SymptomUpdateForm(forms.ModelForm):
    class Meta:
        model = SymptomUpdate
        fields = ['symptoms']
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your current symptoms...'
            })
        }
