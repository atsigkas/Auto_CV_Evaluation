from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from . import main
from .ResumeParser.ExtractInfo_part1_python import pdf_extractor
from .main import ranking
from .Scrapers.main_scrapy import update_candidate_profile

import json


# Create your views here.


@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')

        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        else:
            for filename in os.listdir('uploads'):
                os.remove(os.path.join('uploads', filename))

        for uploaded_file in files:
            with open(f'uploads/{uploaded_file.name}', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        candidates = main.find_candidate()

        return JsonResponse({'message': 'Files uploaded successfully!','candidates': candidates})

    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
def save_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        _id = request.POST.get('_id')

        candidate = update_candidate_profile(_id, url)

        return JsonResponse({'message': 'Candidate Url successfully saved', 'candidate': candidate})

    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
def ranking_candidates(request):
    if request.method == 'POST':

        NotFoundPublications = json.loads(request.POST.get('NotFoundPublications'))
        candidates = json.loads(request.POST.get('candidates'))
        positionTitle = request.POST.get('positionTitle')
        positionDescription = request.POST.get('positionDescription')

        rankings = ranking(NotFoundPublications,candidates,positionTitle,positionDescription)
        print(rankings)
        return JsonResponse({'message': 'Ranking is calculated', 'rankings': rankings})

    return JsonResponse({'message': 'Invalid request method'}, status=400)


