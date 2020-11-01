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
    if request.method == 'POST':
        count = int(request.POST.get('next_count', 10))
    else:
        count = 10
    data_file = get_object_or_404(CollectionFile, pk=file_id)
    table_as_html = petl.MemorySource()
    data_file.get_table().head(count).tohtml(table_as_html)
    return render(request, 'swcollections/file_data.html', {
        'next_count': count + 10,
        'filename': data_file.file_name(),
        'filedata': table_as_html.getvalue().decode('utf-8'),
    })
