from random import Random
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UrlForm,DetailsForm
from pytube import Playlist, YouTube
import os
from moviepy.editor import *

def index(request):
    form = UrlForm()
    return render(request,'downloader/index.html', {'form': form})


def details(request):
    thumb = ""
    if request.method == 'GET':
        url = request.GET.get('url')
        request.session["url"] = url
        
        if 'playlist' not in url:
            video = YouTube(url)
            youtube_title = video.title
        elif 'playlist' in url:
            video = Playlist(url).videos[0]
            youtube_title = Playlist(url).title
    
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            only_audio = form.cleaned_data['audio_or_video']
            url = request.session["url"]
            if 'playlist' in url:
                download_playlist(url, "./downloads",only_audio)
            else:
                download_video(url, "./downloads",only_audio)
            
            return render(request,'downloader/success.html')
    else:
        form = DetailsForm()
    return render(request,'downloader/download.html', {'form': form, 'yt_video': video, 'youtube_title': youtube_title})


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
            out_file = yout.streams.filter(progressive=True,mime_type='video/mp4').first().download(path)
            videoclip = VideoFileClip(out_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(out_file[0:-4] + '.mp3',ffmpeg_params=['-metadata', 'title='+yout.title,'-metadata', 'artist='+yout.author,'-metadata', 'album='+yout.author])
            videoclip.close()
            audioclip.close()
            os.remove(out_file)
        else:
            yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)
    

def download_video(url, path:str,only_audio=False):
    yout = YouTube(url)
    yout.register_on_progress_callback(on_progress)
    if only_audio == "True":
        out_file = yout.streams.filter(progressive=True,mime_type='video/mp4').first().download(path)
        videoclip = VideoFileClip(out_file)
        audioclip = videoclip.audio
        audioclip.write_audiofile(out_file[0:-4] + '.mp3',ffmpeg_params=['-metadata', 'title='+yout.title,'-metadata', 'artist='+yout.author,'-metadata', 'album='+yout.author])
        videoclip.close()
        audioclip.close()
        os.remove(out_file)
    else:
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)
