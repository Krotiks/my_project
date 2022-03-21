from django.shortcuts import render
from . import models

# Create your views here.


def all_ads(request):
    ads = models.Ad.objects.all()
    return render(request, "ads/all_ads.html",
                  {"ads": ads})

