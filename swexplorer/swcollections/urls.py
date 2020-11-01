from django.urls import path
from . import views

urlpatterns = [
    path('fetch', views.fetch_collection, name='fetch-collection'),
    path('', views.FileList.as_view(), name='file-list'),
]
