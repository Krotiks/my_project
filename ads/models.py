from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Ad(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            unique_for_date='publish')

    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_ads')
    publish = models.DateTimeField(default=timezone.now)

    AD_TYPES = [
        ('property', 'Недвижимость'),
        ('auto', 'Авто'),
        ('tech', 'Электроника'),
        ('clothes', 'Одежда'),
        ('kids', 'Детские товары'),
        ('entertainment', 'Развлечения'),
        ('services', 'Услуги'),
    ]
    ad_types = models.CharField(max_length=25,
                                     choices=AD_TYPES,
                                     default='property')

    # def __str__(self):
      #  return self.title

    def get_absolute_url(self):
        return reverse('ads:detailed_ad',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
