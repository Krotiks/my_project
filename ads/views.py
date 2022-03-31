from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import models
from . import forms

# Create your views here.


def all_ads(request):
    ads = models.Ad.objects.all()
    return render(request, "ads/all_ads.html",
                  {"ads": ads})


@login_required
def detailed_ad(request, yy, mm, dd, slug):
    ad = get_object_or_404(models.Ad,
                           publish__year=yy,
                           publish__month=mm,
                           publish__day=dd,
                           slug=slug)
    return render(request, "ads/detailed_ad.html",
                  {"ad": ad})

def share_ad(request, ad_id):
    ad = get_object_or_404(models.Ad, id=ad_id)
    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ad_uri = request.build_absolute_uri(
                ad.get_absolute_url()
            )
            subject = 'Someone shared with you ads' + ad.title
            body_template = ('On our site someone post an ads. ' \
                   '\n\nlink to material: {link}' \
                   '\n\ncomment: {comment}')
            body = body_template.format(link=ad_uri,
            comment = cd['comment'])
            send_mail(subject, body, 'admin@my.com', (cd['to_email'],))
    else:
        form = forms.EmailMaterialForm()
    return render(request,
                  'ads/share.html',
                  {'ad': ad, 'form' : form})


def create_ad(request):
    if request.method == 'POST':
        ad_form = forms.AdForm(request.POST)
        if ad_form.is_valid():
            new_ad = ad_form.save(commit=False)
            new_ad.author = User.objects.first()
            new_ad.slug = new_ad.title.replace(' ', '_')
            new_ad.save()
            return render(request, "ads/detailed_ad.html",
                          {"ad": new_ad})
    else:
        ad_form = forms.AdForm()
    return render(request,
                  'ads/create.html',
                  {'form': ad_form})


def custom_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'],
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('user was logged in')
                else:
                    return HttpResponse('user is not active')
            else:
                return HttpResponse('user not found')
    else:
        form = forms.LoginForm()
    return render(request,
                  'login.html',
                  {'form': form})
