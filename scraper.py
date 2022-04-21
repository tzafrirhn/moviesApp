import requests
import urllib.parse
from os import environ

TMDB_KEY = environ['PROJ_TMDB_KEY']

class TMDBScraper:

    URL_CNF = 'http://api.themoviedb.org/3/configuration?api_key={KEY}'
    search = {
        'by_imdb_id': 'https://api.themoviedb.org/3/movie/{ID}/images?api_key={KEY}',
        'by_name': 'https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={QUERY}',
    }

    def __init__(self, key=TMDB_KEY):
        self.key = key
        self.conf = self.get_config()

    def get_config(self):
        query = self.URL_CNF.format(KEY=self.key)
        response = requests.get(query)
        if response.status_code != 200:
            raise Exception
        return response.json()

    def search_ids(self, name):
        query = self.search['by_name'].format(KEY=self.key, QUERY=urllib.parse.quote(name))
        response = requests.get(query)
        return [x['id'] for x in response.json()['results']]

    def get_img(self, id):
        query = self.search['by_imdb_id'].format(KEY=self.key, ID=id)
        response = requests.get(query)
        return [f"{self.conf['images']['base_url']}original{x['file_path']}" for x in response.json()['posters']]


if __name__ == "__main__":
    scraper = TMDBScraper()
    ids = scraper.search_ids('batman')
    urls = scraper.get_img(ids[0])
    for url in urls:
        print(url)
