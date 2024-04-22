from django.urls import path
from . import views
from .views.index_view import IndexView
from .views.details_view import DetailsView

urlpatterns = [
    path('download', DetailsView.as_view(), name='details'),
    path('', IndexView.as_view(), name='index'),
]