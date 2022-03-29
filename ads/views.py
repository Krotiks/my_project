from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from . import models
from . import forms

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
