import petl
import requests
from functools import lru_cache


# Idea for improvement: make URL to SWAPI configurable


class PlanetCache:
    def __init__(self):
        self._cache = None

    def get_planet(self, resource):
        if self._cache is None:
            self._cache = dict(
                (planet['url'], planet['name'])
                for planet
                in get_all_from('https://swapi.dev/api/planets/')
            )
        return self._cache[resource]


PLANET_CACHE = PlanetCache()


# With the amount of data that is available now this strategy
# results in fewer requests and is therefore faster. 
def get_homeworld_name(resource):
    return PLANET_CACHE.get_planet(resource)


# @lru_cache
# def get_homeworld_name(resource):
#     response = requests.get(resource)
#     data = response.json()
#     return data['name']


def get_all_from(url, page_size=100):
    separator = '&' if '?' in url else '?'
    url = f'{url}{separator}page_size={page_size}'
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
