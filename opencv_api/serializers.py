from rest_framework import serializers


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
    current_progress = serializers.IntegerField()
    faces_count = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'status': instance.status,
            'current_progress': instance.current_progress,
            'result_aggregation': {
                'faces_count': instance.faces_count,
            }
        }


class IdVideoSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'video_id': str(instance.id),
        }


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
