from django.shortcuts import render
from .forms import VideoUploadForm
from django.conf import settings
from asgiref.sync import sync_to_async
from .vdface_algorithm import opencv_detect
import requests


async def main_view(request):
    return render(request, 'opencv_api/main.html', {})


def vdface_view(request):
    # loop = asyncio.get_event_loop()
    form = VideoUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            videoURL = settings.MEDIA_URL + form.instance.document.name
            # loop.create_task(opencv_detect(settings.MEDIA_ROOT_URL + videoURL))
            d = opencv_detect(settings.MEDIA_ROOT_URL + videoURL, form.instance.document.name).copy()
            return render(request, 'opencv_api/vdface.html', {'form': form,
                                                              'post': post,
                                                              'current_progress': d['current_progress'],
                                                              'faces_count': d['faces_count']})
    else:
        form = VideoUploadForm()
    return render(request, 'opencv_api/vdface.html', {'form': form})


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoUploadModel
from .serializers import VideoSerializer


class UploadVideoView(APIView):
    def get(self, request):
        videos = VideoUploadModel.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response({"videos": serializer.data})

    def post(self, request):
        pass


class CancelUploadVideoView(APIView):
    def post(self, request):
        pass