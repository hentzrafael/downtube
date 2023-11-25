from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label="Youtube Playlist URL",max_length=200)
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, 'Playlist'), (2, 'Video')],label="Escolha o tipo:",required=True)
    audio_or_video = forms.ChoiceField(widget=forms.RadioSelect, choices=[(True, 'Audio'), (False, 'Video')],label="Escolha o tipo do arquivo:",required=False)
