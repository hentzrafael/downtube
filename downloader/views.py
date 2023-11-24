from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UrlForm
from pytube import Playlist, YouTube

def index(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            #TODO: download the video
            download_playlist(url, "./tmp")
    else:
        form = UrlForm()
    return render(request,'downloader/index.html', {'form': form})

def download_playlist(url, path):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item)
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)

