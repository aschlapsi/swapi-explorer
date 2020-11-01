import petl
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView
from swcollections.models import CollectionFile, fetch_characters


class FileList(ListView):
    model = CollectionFile
    context_object_name = 'collection_files'


def fetch_collection(request):
    fetch_characters()
    return redirect('file-list')


def display_file_data(request, file_id):
    data_file = get_object_or_404(CollectionFile, pk=file_id)
    table_as_html = petl.MemorySource()
    data_file.get_table().head(10).tohtml(table_as_html)
    return render(request, 'swcollections/file_data.html', {
        'filename': data_file.file_name(),
        'filedata': table_as_html.getvalue().decode('utf-8'),
    })
