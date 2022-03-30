from django import forms
from . import models


class EmailMaterialForm(forms.Form):
    to_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)


class AdForm(forms.ModelForm):
    class Meta:
        model = models.Ad
        fields = ('title', 'text', 'ad_types')
