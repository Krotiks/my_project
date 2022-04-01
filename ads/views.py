from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import redirect
from . import models
from . import forms

# Create your views here.
class AdListView(LoginRequiredMixin, ListView):
    queryset = models.Ad.objects.all()
    context_object_name = 'ads'
    template_name = "ads/all_ads.html"


#def all_ads(request):
#    ads = models.Ad.objects.all()
#    return render(request, "ads/all_ads.html",
#                 {"ads": ads})


@login_required
def detailed_ad(request, yy, mm, dd, slug):
    ad = get_object_or_404(models.Ad,
                           publish__year=yy,
                           publish__month=mm,
                           publish__day=dd,
                           slug=slug)
    ads = models.Ad.objects.all()
    if request.method == "POST":
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.ad = ad
            new_comment.save()
            return redirect(ad)
    else:
        comment_form = forms.CommentForm()

    return render(request, "ads/detailed_ad.html",
                  {"ad": ad,
                   "form": comment_form,
                   "ads": ads})


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
            body_template = ('On our resource someone shared material with '
                             'you. \n\nlink to material: {link}\n\ncomment: '
                             '{comment}')
            body = body_template.format(link=ad_uri,
                                        comment=cd['comment'])
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


def view_profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == "POST":
        user_form = forms.RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user, photo="unknown.jpg")
            return render(request, 'registration/registration_complete.html',
                          {'new_user': new_user})
        else:
            return HttpResponse('bad credentials')
    else:
        user_form = forms.RegistrationForm(request.POST)
        return render(request, 'registration/register_user.html', {"form": user_form})
