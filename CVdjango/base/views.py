from django.shortcuts import render
from django.http import HttpResponse
from .db import utils
from .scrapers import main

# Create your views here.


def home(request):
    scraper_google_scolar.fetch_data()
    return render(request, 'home.html')

