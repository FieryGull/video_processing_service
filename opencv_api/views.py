import io
import requests

from django.shortcuts import render
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from opencv_api import tasks
from django.db import Error
from .models import VideoUploadModel
from .serializers import VideoSerializer, IdVideoSerializer, ErrorSerializer
from .forms import VideoUploadForm


async def main_view(request):
    form = VideoUploadForm()
    try:
        videos = requests.get('http://127.0.0.1:8000/processing/video/')
        stream = io.BytesIO(videos.content)
        data = JSONParser().parse(stream)['videos']
        return render(request, 'opencv_api/main.html', {'form': form, 'data': data})
    except Exception:
        pass
    return render(request, 'opencv_api/main.html', {'form': form})


class UploadVideoView(APIView):
    def get(self, request):
        try:
            videos = VideoUploadModel.objects.all()
            serializer = VideoSerializer(videos, many=True)
            return Response({"videos": serializer.data})
        except Exception:
            error = 'Произошла ошибка получения видео'
            error_serializer = ErrorSerializer(error)
            return Response(error_serializer.data[0], status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                tasks.process_video.delay(post.id)
                video = VideoUploadModel.objects.filter(id=post.id)
                serializer = IdVideoSerializer(video, many=True)
                return Response(serializer.data[0])
        except Exception:
            error = 'Произошла ошибка загрузки видео'
            error_serializer = ErrorSerializer(error)
            return Response(error_serializer.data[0], status=HTTP_400_BAD_REQUEST)


class CancelUploadVideoView(APIView):
    def post(self, request, pk):
        try:
            VideoUploadModel.objects.filter(id=pk).update(status="canceled")
            return Response(status=status.HTTP_200_OK)
        except Error:
            error = 'Произошла ошибка отмены обработки'
            error_serializer = ErrorSerializer(error)
            return Response(error_serializer.data[0], status=HTTP_400_BAD_REQUEST)
