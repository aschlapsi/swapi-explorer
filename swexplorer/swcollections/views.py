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
    table_output = petl.MemorySource()
    table = data_file.get_table()
    table.head(count).tohtml(table_output)
    return render(request, 'swcollections/file_data.html', {
        'next_count': count + 10,
        'file': data_file,
        'filename': data_file.file_name(),
        'filedata': table_output.getvalue().decode('utf-8'),
        'can_load_more': count < table.nrows(),
    })


def analyze_file_data(request, file_id):
    data_file = get_object_or_404(CollectionFile, pk=file_id)
    active_headers = request.POST.get('active', '')
    active_headers = active_headers.split(',')
    active_headers = [header for header in active_headers if header]

    if request.method == 'POST':
        header_to_activate = request.POST['activate']
        if header_to_activate in active_headers:
            active_headers.remove(header_to_activate)
        else:
            active_headers.append(header_to_activate)

    table = data_file.get_table()
    headers = table.fieldnames()

    if len(active_headers) > 0:
        key = active_headers
        if len(key) == 1:
            key = active_headers[0]
        table_output = petl.MemorySource()
        table.aggregate(key=key, aggregation=len).tohtml(table_output)
        table_html = table_output.getvalue().decode('utf-8')
    else:
        table_html = ''

    return render(request, 'swcollections/analyze_file_data.html', {
        'headers': headers,
        'active_headers': active_headers,
        'file': data_file,
        'filename': data_file.file_name(),
        'filedata': table_html,
    })
