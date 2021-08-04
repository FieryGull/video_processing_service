from django.contrib import admin
from .models import VideoUploadModel


@admin.register(VideoUploadModel)
class UploadAdmin(admin.ModelAdmin):
    pass
