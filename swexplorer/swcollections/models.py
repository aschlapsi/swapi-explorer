import uuid
from pathlib import Path
from django.conf import settings
from django.conf import settings
from django.db import models
from swcollections import swapi


def get_new_csv_file_path():
    base_path = Path(settings.LOCAL_FILE_DIR)
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path / f'{uuid.uuid4()}.csv'


def fetch_characters():
    file_path = get_new_csv_file_path()
    collection_file = CollectionFile(csv_file_path=file_path)
    swapi.fetch_characters(file_path)
    collection_file.save()
    return collection_file


class CollectionFile(models.Model):
    csv_file_path = models.FilePathField(path=settings.LOCAL_FILE_DIR, match=r'.*\.csv')
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.csv_file_path
