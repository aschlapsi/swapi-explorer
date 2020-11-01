import petl
import requests
from functools import lru_cache


@lru_cache
def get_homeworld_name(resource):
    response = requests.get(resource)
    data = response.json()
    return data['name']


def get_all_from(url):
    while True:
        response = requests.get(url)
        data = response.json()
        for row in data['results']:
            yield row
        url = data['next']
        if not url:
            break


def fetch_characters(file_path):
    header = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'edited']
    people_dicts = get_all_from('https://swapi.dev/api/people/')
    table = (
        petl.io.json.fromdicts(people_dicts, header=header)
            .rename('edited', 'date')
            .convert('date', lambda timestamp: timestamp[:10])
            .convert('homeworld', get_homeworld_name)
    )
    table.tocsv(file_path)