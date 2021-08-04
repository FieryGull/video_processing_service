from django.conf.urls import url
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('vdface/', views.vdface_view, name='vdface'),
    path('', views.main_view, name='main'),
    path('processing/video/', views.UploadVideoView.as_view(), name='video')
]