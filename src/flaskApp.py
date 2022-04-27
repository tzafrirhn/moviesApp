from flask import Flask, request, redirect, url_for, session, make_response, render_template_string
import requests
from mongoCRUD import posterStorage, cache
from scraper import TMDBScraper
from secrets import token_hex
from sys import stderr as out
from urllib.parse import quote

app = Flask(__name__, template_folder='templates')
app.secret_key = str(token_hex(1024))

@app.route('/posters/<name>')
def show_poster(name):
    poster = posters.find(name)
    if poster is None:
        return make_response("Not found", 404)
    return poster.read()
    # def send():
    #     for row in poster: yield row
    # response = Response(send())
    # response.content_type = "image/webp"
    # return response


blob_image = """
<img src='{url}' />
"""

blob_link = """
<a class="poster_link" href='{base}?psearch={srch}&selected_img={nr}'>
<div class="poster_div">
{name}
</div>
</a>
"""

@app.route('/')
def searchPoster():
    args = request.args

    [results, images] = maybe_render_img(args)

    images = '{% block images %}'+''.join([
        blob_image.format(url=x)
        for x in images
    ])+'{% endblock %}'

    results = '{% block results %}'+''.join([
        blob_link.format(base=request.base_url, srch=quote(args['psearch']), nr=x[0], name=x[1])
        for x in enumerate(results)
    ])+'{% endblock %}'
    ######## fix psearch don't exist
    psearch = '{% block search %}' + args.get('psearch', '') + '{% endblock %}'
    title='{% block title %}'+args.get('psearch', '')+'{% endblock %}'

    return render_template_string('{% extends "index.html" %} '+results+images+psearch+title)

def log(*args, **kwargs):
    print("="*80)
    print(*args, file=out)
    for [k, v] in kwargs.items():
        print(k, ':', v, file=out)
    print("="*80)

def maybe_render_img(args):

    if 'psearch' not in args.keys(): return ((), ())
    selected_img = int(args.get('selected_img', 0))

    results = cached.search_by_name(args['psearch']) #search in mongodb
    if len(results) == 0:
        results = scraper.search_by_name(args['psearch']) #if not found search in tmdb
        cached.put(results, args['psearch']) # save poster in tmdb
    if len(results) == 0: return ((), ()) #if results empty from tmdb

    selected_image = results[selected_img]

    log(selected_image)
    movie_images = [
        find_or_add(x['file_path']) for x in
        scraper.search_by_id(selected_image['id'])['posters'][:5]
    ]

    log(movie_images)

    return ([x['original_title'] for x in results], movie_images) # return poster list

#return url for selected image
def find_or_add(url):
    fname = url.lstrip('/')
    exists = posters.find(fname)
    if exists:
        # log('find_or_add', exists)
        return url_for('show_poster', name=exists.name.lstrip('/'))

    url = scraper.make_img_url(url)
    req = requests.get(url)
    posters.save(name=fname, data=req.content)
    new = url_for('show_poster', name=fname)
    # log('new: ', new)
    return new


if __name__ == "__main__":
    posters = posterStorage()
    scraper = TMDBScraper()
    cached  = cache()
    app.run(host='0.0.0.0', debug=True)
