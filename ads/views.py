from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . import models

# Create your views here.


def all_ads(request):
    ads = models.Ad.objects.all()
    return render(request, "ads/all_ads.html",
                  {"ads": ads})


def detailed_ad(request, yy, mm, dd, slug):
    ad = get_object_or_404(models.Ad,
                           publish__year=yy,
                           publish__month=mm,
                           publish__day=dd,
                           slug=slug)
    return render(request, "ads/detailed_ad.html",
                  {"ad": ad})
