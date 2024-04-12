from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3 '},)
        )

class DetailsForm(forms.Form):
    audio_or_video = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check'}), choices=[(True, 'Audio'), (False, 'Video')],label="Escolha o tipo do arquivo:",required=True)
    