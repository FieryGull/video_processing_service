from celery import shared_task
from django.conf import settings

from opencv_api import models
from opencv_api.vdface_algorithm import opencv_detect


@shared_task
def process_video(video_id: int):
    print('Start video processing')
    obj = models.VideoUploadModel.objects.get(id=video_id)
    video_url = f'{settings.MEDIA_ROOT_URL}{settings.MEDIA_URL}{obj.document.name}'
    opencv_detect(video_url, video_id)
    print('END video processing')
