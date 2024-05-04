from django.urls import path
from . import views
from .views.index_view import IndexView
from .views.details_view import DetailsView
from .views.download_view import DownloadView

urlpatterns = [
    path('download', DownloadView.as_view(), name='download'),
    path('details', DetailsView.as_view(), name='details'),
    path('', IndexView.as_view(), name='index'),
]