import os.path

import requests
import collections

URL = 'https://api.mangadex.dev/'
DICT_REQUESTS = {'manga': '/manga',
                 'chapter': '/chapter',
                 'cover': '/cover'}


class ApiFetcher:
    def get_manga_dict(self, manga_name):
        response = requests.get(f"{URL}{DICT_REQUESTS['manga']}?title={manga_name}")
        if response.status_code == 200:
            response = response.json()['data']
            return response
        else:
            return None

    def get_chapters(self, manga_id):
        response = requests.get(f"{URL}{DICT_REQUESTS['manga']}/{manga_id}{DICT_REQUESTS['chapter']}")
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(response.status_code)
            return None

    def get_cover(self, manga_id, limit=100):
        dict_cover = {}
        params = {'manga[]': manga_id, 'limit': limit}
        response = requests.get(f"{URL}{DICT_REQUESTS['cover']}", params=params)
        if response.status_code == 200:
            response = response.json()
            for cover_vol in response['data']:
                dict_cover[int(cover_vol['attributes']['volume'])] = cover_vol['attributes']['fileName']
            dict_cover = collections.OrderedDict(sorted(dict_cover.items()))
            return dict_cover
        else:
            print(response.status_code)
            return None

    def set_manga_data(self, manga_name):
        dict_manga = {}
        manga_data = self.get_manga_dict(manga_name)

        for manga in manga_data:
            dict_manga['id'] = manga['id']
            dict_manga['title'] = manga['attributes']['title']['en']
            dict_manga['status'] = manga['attributes']['status']
            dict_manga['year'] = manga['attributes']['year']
            return dict_manga


class Manga(ApiFetcher):
    def __init__(self, manga_name):
        self.manga_data = self.set_manga_data(manga_name)
        self.id = self.manga_data['id']
        self.title = self.manga_data['title']
        self.year = self.manga_data['year']
        self.status = self.manga_data['status']
        self.cover_dict = self.get_cover(self.id)

    def download_covers(self):
        pass


jujutsu = Manga('jujutsu kaisen')

print(jujutsu.cover_dict)

