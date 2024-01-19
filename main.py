import os.path
import time

import requests
import collections

# url para as jpgs https://uploads.mangadex.org/covers/:manga-id/:cover-filename

URL = 'https://api.mangadex.dev/'
DICT_REQUESTS = {'manga': '/manga',
                 'chapter': '/chapter',
                 'cover': '/cover'}
URL_UPLOAD = 'https://uploads.mangadex.org/covers/'


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

    def download_image(self, url, filename, retries=3):
        for _ in range(retries):
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(filename, 'wb') as file:
                        print(f"Downloading {filename}...")
                        for chuck in response.iter_content(1024):
                            file.write(chuck)
                return
            except requests.exceptions.ChunkedEncodingError as e:
                print(f"Download failed for {url}, error {e} retrying...")
                time.sleep(1)
        print(f"Failed to download image from {url} after {retries} attempts")

    def download_images(self, url_lists, folder_path):
        for i, url in enumerate(url_lists):
            filename = os.path.join(folder_path, f'{self.title}_cover_vol{i}.jpg')
            self.download_image(url, filename)

    def download_covers(self, folder_path):
        url_list = [URL_UPLOAD + f"{self.id}/{cover_filename}" for cover_filename in self.cover_dict.values()]
        self.download_images(url_list, folder_path)


jujutsu = Manga('jujutsu kaisen')
jujutsu.download_covers('cover')


print(jujutsu.cover_dict)

