from django.db import models

# Create your models here.
from django.db import models

class PublicationPDF(models.Model):
    title = models.CharField(max_length=255)
    researchgate_url = models.URLField(blank=True)
    googleScholar_url = models.URLField(blank=True)
    sematic_url = models.URLField(blank=True)

class Publication(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, blank=True)
    abstract = models.TextField(blank=True)
    citation = models.CharField(max_length=255, blank=True)
    topics = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)

class ResearchGate(models.Model):
    author_id = models.CharField(max_length=255)
    author_url = models.URLField()
    publications = models.ManyToManyField(Publication)

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    publicationpdf = models.ForeignKey(PublicationPDF, on_delete=models.CASCADE)
