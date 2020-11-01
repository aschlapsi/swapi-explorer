from django.shortcuts import redirect
from django.views.generic import ListView
from swcollections.models import CollectionFile, fetch_characters


class FileList(ListView):
    model = CollectionFile
    context_object_name = 'collection_files'


def fetch_collection(request):
    fetch_characters()
    return redirect('file-list')
