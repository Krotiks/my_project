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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'body')