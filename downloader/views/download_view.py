from django.views.generic import TemplateView
from django.shortcuts import render
from downloader.tasks import download_playlist, download_video


class DownloadView(TemplateView):
    template_name = 'downloader/download.html'

    def get(self, request, *args, **kwargs):
        url = request.session["url"]
        only_audio = request.GET.get('audio_or_video')
        if 'playlist' in url:
            task = download_playlist.delay(url, "./downloads",only_audio)
        else:
            task = download_video.delay(url, "./downloads",only_audio)
        return render(request,self.template_name,{'task_id': task.task_id})