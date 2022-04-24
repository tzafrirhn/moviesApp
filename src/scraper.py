import requests
import urllib.parse
from os import environ
from mongoCRUD import cache

TMDB_KEY = environ['PROJ_TMDB_KEY']

class TMDBScraper:

    URL_CNF = 'http://api.themoviedb.org/3/configuration?api_key={KEY}'
    search = {
        'by_imdb_id':
        'https://api.themoviedb.org/3/movie/{ID}/images?api_key={KEY}',
        'by_name':
        'https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={QUERY}&page={PAGE}',
    }

    def __init__(self, key=TMDB_KEY):
        self.key = key
        self.conf = self.get_config()

    def make_img_url(self, img_rel_url):
        return self.conf['images']['base_url'] + "original" + img_rel_url

    def get_config(self):
        query = self.URL_CNF.format(KEY=self.key)
        with requests.get(query) as response:
            return response.json()

    def search_by_name(self, name):
        page_nr = 1
        results = []
        def mkquery(): return self.search['by_name'].format(KEY=self.key, PAGE=page_nr, QUERY=urllib.parse.quote(name))
        with requests.Session() as conn:
            resp = conn.get(mkquery()).json()
            last_page = resp['total_pages']
            results.extend(resp['results'])
            while page_nr < last_page:
                page_nr += 1
                resp = conn.get(mkquery())
                results.extend(resp.json()['results'])
            return results

    # def describe_movies(self, movies):
    #     with requests.Session() as conn:
    #         for movie in movies:
    #             query = self.search['by_imdb_id'].format(KEY=self.key, ID=movie['id'])
    #             movie['info'] = conn.get(query)
    #     return movies

    def search_by_id(self, id):
        query = self.search['by_imdb_id'].format(KEY=self.key, ID=id)
        with requests.get(query) as response:
            return response.json()

    def search_ids(self, name):
        results = self.search_by_name(name)
        return [x['id'] for x in results]

    def get_img(self, id):
        results = self.search_by_id(id)
        return [
            self.make_img_url(x['file_path'])
            for x in results['posters']
        ]

if __name__ == "__main__":
    scraper = TMDBScraper()

    test = scraper.search_by_name('batman')
    for x in test:
        print(x['original_title'])

    movie = scraper.search_by_id(test[0]['id'])
    print(movie.keys())
