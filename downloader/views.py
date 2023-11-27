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
            if 'playlist' in url:
                download_playlist(url, "./tmp",only_audio=audio_or_video)
            else:
                download_video(url, "./tmp",only_audio=audio_or_video)
    else:
        form = UrlForm()
    return render(request,'downloader/index.html', {'form': form})

def on_progress(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    progress = (bytes_downloaded / total_bytes) * 100
    print(f"Download progress: {progress:.2f}%")
    return f"<script>updateProgressBar({progress})</script>"

def download_playlist(url, path,only_audio=False):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item,on_progress_callback=on_progress)
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
