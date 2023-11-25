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
            audio_or_video = form.cleaned_data['audio_or_video']
            tipo = form.cleaned_data['tipo']
            if tipo == '1':
                download_playlist(url, "./tmp",only_audio=audio_or_video)
            elif tipo == '2':
                download_video(url, "./tmp",only_audio=audio_or_video)
            
    else:
        form = UrlForm()
    return render(request,'downloader/index.html', {'form': form})

def download_playlist(url, path,only_audio=False):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item)
        if only_audio == "True":
            yout.streams.get_audio_only().download(path, filename_prefix=str(time.time()),filename="audio.mp3")
        else:
            yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path, filename_prefix=str(time.time()))

def download_video(url, path,only_audio=False):
    yout = YouTube(url)
    if only_audio == "True":
        yout.streams.get_audio_only().download(path, filename_prefix=str(time.time()),filename="audio.mp3")
    else:
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path, filename_prefix=str(time.time()))
