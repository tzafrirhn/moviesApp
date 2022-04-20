import requests
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
KEY = '192ee0157eb9c506ee39de6c95e00873'

url = CONFIG_PATTERN.format(key=KEY)
r = requests.get('https://api.themoviedb.org/3/configuration?api_key=192ee0157eb9c506ee39de6c95e00873')
config = r.json()
print(config)
base_url = config['images']['base_url']
sizes = config['images']['poster_sizes']
"""
    'sizes' should be sorted in ascending order, so
        max_size = sizes[-1]
    should get the largest size as well.        
"""
def size_str_to_int(x):
    return float("inf") if x == 'original' else int(x[1:])
max_size = max(sizes, key=size_str_to_int)
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
r = requests.get(IMG_PATTERN.format(key=KEY,imdbid='tt0095016'))
api_response = r.json()
print(api_response)
posters = api_response['posters']
poster_urls = []
for poster in posters:
    rel_path = poster['file_path']
    url = "{0}{1}{2}".format(base_url, max_size, rel_path)
    poster_urls.append(url)
for nr, url in enumerate(poster_urls):
    r = requests.get(url)
    filetype = r.headers['content-type'].split('/')[-1]
    filename = 'poster_{0}.{1}'.format(nr+1,filetype)
    with open(filename,'wb') as w:
        w.write(r.content)