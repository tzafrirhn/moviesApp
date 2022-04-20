from flask import Flask, request, redirect, url_for
app = Flask(__name__)

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
    app.run()
