# views.py
import json 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse
import os
import requests
from dotenv import load_dotenv
from vw_storages.settings import BASE_DIR
from django.http import JsonResponse, HttpResponse


load_dotenv()
sia_url = os.environ.get('SIA_URL')
sia_code = os.environ.get('SIA_CODE')

#SIA APIs will be updated using celery

class VideoUploadViewSIA(APIView):
    def post(self, request, *args, **kwargs):

        # Download file contents as binary
        file_url = request.data['file_url']
        parsed_url = urlparse(file_url)
        filename = parsed_url.path.split("/")[-1]
        url = f"{sia_url}api/worker/objects/videowiki/{filename}"

        resp = requests.get(file_url)
        binary_data = resp.content

        headers = {
            'Content-Type': 'video/webm',
            'Authorization': f'Basic {sia_code}'
        }

        response = requests.put(url, headers=headers, data=binary_data)

        return Response(response.text, status=response.status_code)


class VideoDownloadViewSIA(APIView):
    def get(self, request, *args, **kwargs):
        file_name = request.GET.get('file_name')

        headers = {
            'Authorization': f'Basic {sia_code}',
            'Content-Type': 'video/webm'
        }
        url = f"{sia_url}api/worker/objects/videowiki/{file_name}"

        # Send GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            binary_data = response.content

            return HttpResponse(binary_data, content_type='video/webm')
        else:
            return JsonResponse({'error': 'Failed to download file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


