from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UrlForm,DetailsForm
from pytube import Playlist, YouTube
import time

def index(request):
    form = UrlForm()
    return render(request,'downloader/index.html', {'form': form})


def details(request):
    thumb = ""
    if request.method == 'GET':
        url = request.GET.get('url')
        request.session["url"] = url
    
        if 'playlist' not in url:
            thumb = YouTube(url).thumbnail_url
    
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            only_audio = form.cleaned_data['audio_or_video']
            url = request.session["url"]
            if 'playlist' in url:
                download_playlist(url, "./tmp",only_audio)
            else:
                download_video(url, "./tmp",only_audio)
            
            return render(request,'downloader/success.html')
    else:
        form = DetailsForm()
    return render(request,'downloader/download.html', {'form': form, 'thumb': thumb})


def on_progress(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    progress = (bytes_downloaded / total_bytes) * 100
    print(f"Download progress: {progress:.2f}%")

def download_playlist(url, path,only_audio=False):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item)
        yout.register_on_progress_callback(on_progress)
        if only_audio == "True":
            yout.streams.get_audio_only().download(path,filename=f"{yout.title}.mp3")
        else:
            yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)

def download_video(url, path,only_audio=False):
    yout = YouTube(url)
    yout.register_on_progress_callback(on_progress)
    if only_audio == "True":
        yout.streams.get_audio_only().download(path,filename=f"{yout.title}.mp3")
    else:
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)
