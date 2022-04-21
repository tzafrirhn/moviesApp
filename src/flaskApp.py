from flask import Flask, request, redirect, url_for, session
import requests
from mongoCRUD import posterStorage
from scraper import TMDBScraper
from secrets import token_hex

app = Flask(__name__)
app.secret_key = str(token_hex(1024))

@app.route('/posters/<name>')
def show_poster(name):
    poster = posters.find(name)
    return poster.read()

@app.route('/')
def searchPoster():
    image = ""
    if 'psearch' in session.keys():
        image = f"""<img src="{url_for('show_poster', name=session['psearch'])}" />"""
        session.pop('psearch', None)
    return f'''<html>
    <body>
    <form action="search">
    <label>Movie Name:</label>
    <input type="search" name="psearch">
    <input type="submit">
    </form>
    {image}
    </body>
    </html>
    '''

@app.route('/search')
def showPoster():
    args = request.args
    if posters.find(args['psearch']) is None:
        id = scraper.search_ids(args['psearch'])
        if not id:
            return redirect(url_for('searchPoster'))
        images = scraper.get_img(id[0])
        img = requests.get(images[0])
        posters.save(name=args['psearch'], data=img.content)

    session['psearch'] = args['psearch']
    return redirect(url_for('searchPoster'))


if __name__ == "__main__":
    posters = posterStorage()
    scraper = TMDBScraper()
    app.run(host='0.0.0.0', debug=True)
