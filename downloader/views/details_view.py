from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from pytube import Playlist, YouTube
from moviepy.editor import *
from downloader.forms import DetailsForm

class DetailsView(TemplateView):
    template_name = 'downloader/details.html'
    
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
