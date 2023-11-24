from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label="Youtube Playlist URL",max_length=200)