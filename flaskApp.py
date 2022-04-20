from flask import Flask, request, redirect, url_for
from mongoCRUD import posterStorage
app = Flask(__name__)

@app.route('/posters/<name>')
def show_poster(name):
    poster = posters.find(name)
    return poster.read()

@app.route('/')
def searchPoster():
    return '''<html>
    <body>
    <form action="search">
    <label>Movie Name:</label>
    <input type="search" name="psearch">
    <input type="submit">
    </form>
    </body>
    </html>
    '''

@app.route('/search')
def showPoster():
    args = request.args
    if 'psearch' not in args.keys():
        return redirect(url_for('searchPoster'))
    return f"""Searched for: {args['psearch']}"""


if __name__ == "__main__":
    posters = posterStorage()
    app.run()