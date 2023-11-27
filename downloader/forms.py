from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label="Youtube URL",max_length=200,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    audio_or_video = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check'}), choices=[(True, 'Audio'), (False, 'Video')],label="Escolha o tipo do arquivo:",required=True)
