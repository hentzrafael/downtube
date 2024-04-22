from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from pytube import Playlist, YouTube
import os
from moviepy.editor import *

from downloader.forms import DetailsForm

class DetailsView(TemplateView):
    template_name = 'downloader/download.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        url = request.GET.get('url')
        request.session["url"] = url
         
        if 'playlist' not in url:
            video = YouTube(url)
            youtube_title = video.title
        elif 'playlist' in url:
            video = Playlist(url).videos[0]
            youtube_title = Playlist(url).title

        form = DetailsForm()
        return render(request,self.template_name, {'form': form, 'yt_video': video, 'youtube_title': youtube_title})
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = DetailsForm(request.POST)
        if form.is_valid():
            only_audio = form.cleaned_data['audio_or_video']
            url = request.session["url"]
            if 'playlist' in url:
                self._download_playlist(url, "./downloads",only_audio)
            else:
                self._download_video(url, "./downloads",only_audio)
            self.template_name = 'downloader/success.html'
            
            return render(request,self.template_name)
    
    def _on_progress(self,stream, chunk, bytes_remaining):
        total_bytes = stream.filesize
        bytes_downloaded = total_bytes - bytes_remaining
        progress = (bytes_downloaded / total_bytes) * 100
        print(f"Download progress: {progress:.2f}%")

    def _download_playlist(self,url, path,only_audio=False):
        yt = Playlist(url)
        for item in yt.video_urls:
            yout = YouTube(item)
            yout.register_on_progress_callback(self._on_progress)
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
    

    def _download_video(self,url, path:str,only_audio=False):
        yout = YouTube(url)
        yout.register_on_progress_callback(self._on_progress)
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
