from django.urls import path
from . import views


urlpatterns = [
    path('<int:file_id>/', views.display_file_data, name='file-data'),
    path('fetch', views.fetch_collection, name='fetch-collection'),
    path('', views.FileList.as_view(), name='file-list'),
]
