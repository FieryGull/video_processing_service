from django import forms
from .models import VideoUploadModel


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUploadModel
        fields = ('document', )
