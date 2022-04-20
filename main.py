import requests
import urllib
from os import environ

KEY = environ['PROJ_TMDB_KEY']

URL_IMG = 'https://api.themoviedb.org/3/movie/{ID}/images?api_key={KEY}'
URL_ID = 'https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={QUERY}'
URL_CNF = 'http://api.themoviedb.org/3/configuration?api_key={KEY}'

"""
https://api.themoviedb.org/3/search/movie?api_key={KEY}&language=en-US&query=die%20hard&page=1&include_adult=false 
https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={QUERY}
base_url = conf['images']['base_url']
"""

def get_config():
    query = URL_CNF.format(KEY=KEY)
    response = requests.get(query)
    return response.json()

def search_ids(name):
    query = URL_ID.format(KEY=KEY,QUERY=urllib.parse.quote(name))
    response = requests.get(query)
    return [x['id'] for x in response.json()['results']]

def get_img(config, id):
    query = URL_IMG.format(KEY=KEY, ID=id)
    response = requests.get(query)
    return [ f"{config['images']['base_url']}original{x['file_path']}" for x in response.json()['posters']]


conf = get_config()
ids = search_ids('batman')
