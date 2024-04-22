from django.views.generic import TemplateView
from django.shortcuts import render

from downloader.forms import UrlForm

class IndexView(TemplateView):
    template_name = 'downloader/index.html'

    def get(self,request):
        form = UrlForm()
        return render(request, self.template_name,{'form': form});
    
