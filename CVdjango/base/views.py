from django.shortcuts import render
from .scrapers import main
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .PARTF.ExtractInfo_part1_python import main
from .scrapers.scrapy_researchgate import update_candidate_profile
from .scrapers.scrapy_researchgate import ranking
import json


# Create your views here.


def home(request):
    #scraper_google_scolar.fetch_data()
    return render(request, 'home.html')


@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        jobTitle = request.POST.get('jobTitle')
        jobDescription = request.POST.get('jobDescription')


        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        else:
            for filename in os.listdir('uploads'):
                os.remove(os.path.join('uploads', filename))

        for uploaded_file in files:
            with open(f'uploads/{uploaded_file.name}', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        candidates = main.PART1(jobTitle,jobDescription)

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
        jobTitle = request.POST.get('jobTitle')
        jobDescription = request.POST.get('jobDescription')
        rankings = ranking(NotFoundPublications,candidates,jobTitle,jobDescription)
        print(rankings)
        return JsonResponse({'message': 'Ranking is calculated', 'rankings': rankings})

    return JsonResponse({'message': 'Invalid request method'}, status=400)


