from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UrlForm
from pytube import Playlist, YouTube
import time

def index(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            only_audio = form.cleaned_data['is_audio']
            download_playlist(url, "./tmp",only_audio=form.cleaned_data['is_audio'])
    else:
        form = UrlForm()
    return render(request,'downloader/index.html', {'form': form})

def download_playlist(url, path,only_audio=False):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item)
        if only_audio:
            yout.streams.get_audio_only().download(path, filename_prefix=str(time.time()))
        else:
            yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path, filename_prefix=str(time.time()))

