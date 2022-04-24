from flask import Flask, request, redirect, url_for, session, make_response
import requests
from mongoCRUD import posterStorage, cache
from scraper import TMDBScraper
from secrets import token_hex
from sys import stderr as out
from urllib.parse import quote

app = Flask(__name__)
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


style = """
* {
  font-family: 'Poppins', sans-serif;
}

body {
  margin: 0;
  overflow: hidden;
}

#search {
}

#content {
  width: 100%;
  background: #f0f0f0;
  float: left;
}

#searchbar {
  line-height: 2em;
  font-size: 1em;
  width: 100%;
  padding: .3em;
}

#searchform {
  text-align: center;
  position: relative;
  margin: 1em auto 1em auto;
  width: 95%;
}

#images {
  padding: 2em;
  overflow-y: auto;
}

#results {
  float: left;
  overflow-y: auto;
  max-width: 20em;
  padding: .4em;
  background: #e0e0e0;
  height: 95%;
}

img {
  max-width: 30%;
  height: auto;
  padding: 1em;
  border-radius: 20% 2em 20% 2em;
  filter: drop-shadow(.3em .5em 1em #888);
}

a > .poster_div {
  padding: .2em;
  white-space: nowrap;
  overflow: hidden;
  padding-left: 1em;
  border-radius: 1em;
  background: #eee;
  margin: .5em;
  color: #403e3c;
}

a:visited > .poster_div {
  background: #d4d4d4;
  color: #808080;
}

a:hover > .poster_div {
  background: #fdf8d5;
  color: #000000;
}

.poster_link {
  text-decoration: unset;
}
"""

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

    images = ''.join([
        blob_image.format(url=x)
        for x in images
    ])

    results = ''.join([
        blob_link.format(base=request.base_url, srch=quote(args['psearch']), nr=x[0], name=x[1])
        for x in enumerate(results)
    ])

    return f'''<html>
    <head>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">

    <style>{style}</style>
    </head>
    <body>
    <div id="search">
    <form id="searchform" action="/">
    <input type="search" id="searchbar" name="psearch" value="{args.get('psearch', '')}">
    <input type="hidden" name="selected_img" value="0">
    </form>
    </div>
    <div id="content">
        <div id=results>{results}</div>
        <div id=images>{images}</div>
    </div>
    </body>
    </html>
    '''

def log(*args, **kwargs):
    print("="*80)
    print(*args, file=out)
    for [k, v] in kwargs.items():
        print(k, ':', v, file=out)
    print("="*80)

def maybe_render_img(args):

    if 'psearch' not in args.keys(): return ((), ())
    selected_img = int(args.get('selected_img', 0))

    results = cached.search_by_name(args['psearch'])
    if len(results) == 0:
        results = scraper.search_by_name(args['psearch'])
        cached.put(results, args['psearch'])
    if len(results) == 0: return ((), ())

    selected_image = results[selected_img]

    log(selected_image)
    movie_images = [
        find_or_add(x['file_path']) for x in
        scraper.search_by_id(selected_image['id'])['posters'][:5]
    ]

    log(movie_images)

    return ([x['original_title'] for x in results], movie_images)


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
