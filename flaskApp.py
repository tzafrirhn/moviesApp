from flask import Flask
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
    #search and upload to mongo function and show poster
    return '''<html>
    <body>
    <form action="search">
    <label>Movie Name:</label>
    <input type="search" name="psearch">
    <input type="submit">
    </form>
    <img src="X">
    </body>
    </html
    '''

app.run(host='localhost')