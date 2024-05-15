from django.urls import path
from sia.views import VideoUploadViewSIA, VideoDownloadViewSIA

urlpatterns = [
    path('sia/upload/', VideoUploadViewSIA.as_view(), name='sia-file-upload'),
    path('sia/download/', VideoDownloadViewSIA.as_view(), name='sia-file-upload'),

]

