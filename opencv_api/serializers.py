from rest_framework import serializers
from .models import VideoUploadModel


class VideoSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # status = serializers.CharField()
    # current_progress = serializers.IntegerField()
    # faces_count = serializers.IntegerField()
    class Meta:
        model = VideoUploadModel
        fields = ['id', 'status', 'current_progress', 'faces_count']
        extra_kwargs = {'result_aggregation': 1}

