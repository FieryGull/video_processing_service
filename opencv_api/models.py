from django.db import models


class VideoUploadModel(models.Model):
    document = models.FileField(upload_to='videos/%Y/%m/%d')
    status = models.CharField(max_length=50, default='waiting')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    current_progress = models.IntegerField(blank=True, default=0)
    faces_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.document

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Загруженные видео'


class ErrorModel(models.Model):
    error = models.CharField(max_length=100)


