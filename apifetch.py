import requests

class ApiFetcher:
    def __init__(self):
        self.url = 'https://api.mangadex.dev/'
        self.dict_requests = {'manga': '/manga',
                              'chapther': '/chapter',
                              'cover': '/cover'}

    def get_manga_id(self, manga_name):
        dict_manga = {}
        response = requests.get(f"{self.url}{self.dict_requests['manga']}?title={manga_name}")
        if response.status_code == 200:
            response = response.json()['data']
            for manga in response:
                dict_manga[manga['attributes']['title']['en']] = manga['id']
            return dict_manga
        else:
            return None

    def get_chapter_id(self):
        pass

    def get_cover_chapter(self):
        pass


class Manga:
    def __init__(self, list_chapter):
        self.list_chapters = list_chapter


api = ApiFetcher()
print(api.get_manga_id('mirai nikki'))