from django import forms
from django.contrib.auth import get_user_model
from .models import FrameComment
User=get_user_model()
class FrameCommentForm(forms.ModelForm):
    class Meta:
        model=FrameComment; fields=['message']
        widgets={'message': forms.Textarea(attrs={'rows':3,'class':'form-control','placeholder':'Describe any discomfort or observations...'})}
class AccountCreationForm(forms.Form):
    role=forms.ChoiceField(choices=User.Roles.choices, widget=forms.Select(attrs={'class':'form-select'}))
    first_name=forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    external_id=forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'P-XXXX / C-XXXX'}))
class PatientClinicianRegistrationForm(forms.Form):
    role = forms.ChoiceField(
        choices=[('patient', 'Patient'), ('clinician', 'Clinician')],
        widget=forms.Select(attrs={'class': 'field-input'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'field-input', 'placeholder': 'email@example.com'})
    )
    external_id = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'P-XXXX or C-XXXX'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field-input', 'placeholder': '••••••••'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field-input', 'placeholder': '••••••••'})
    )

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        cpw = cleaned_data.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data