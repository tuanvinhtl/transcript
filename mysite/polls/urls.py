from django.urls import path
from .views import upload_audio
from .views import transcription_view

urlpatterns = [
    path('upload/', upload_audio, name='upload_audio'),
    path('transcription/', transcription_view, name='transcription'),
]