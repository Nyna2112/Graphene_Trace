from django import forms
from .models import FrameComment


class FrameCommentForm(forms.ModelForm):
    class Meta:
        model = FrameComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your note for this time point...'})
        }
<<<<<<< HEAD
=======
from .models import FrameComment, UploadedPressureFile

class UploadPressureFileForm(forms.ModelForm):
    class Meta:
        model = UploadedPressureFile
        fields = ['file']
>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
