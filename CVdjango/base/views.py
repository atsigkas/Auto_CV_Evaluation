from django.shortcuts import render
from django.http import HttpResponse
from .db import utils
from .scrapers import main
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .PARTF.ExtractInfo_part1_python import main


# Create your views here.


def home(request):
    #scraper_google_scolar.fetch_data()
    return render(request, 'home.html')


@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')  # 'files' is the name attribute in the form input
        jobTitle = request.POST.get('jobTitle')  # Retrieve the first string value
        jobDescription = request.POST.get('jobDescription')  # Retrieve the second string value


        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        else:
            for filename in os.listdir('uploads'):
                os.remove(os.path.join('uploads', filename))

        for uploaded_file in files:
            with open(f'uploads/{uploaded_file.name}', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        rank = main.PART1(jobTitle,jobDescription)

        return JsonResponse({'message': 'Files uploaded successfully!','rank':rank})

    return JsonResponse({'message': 'Invalid request method'}, status=400)
