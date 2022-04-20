from flask import Flask,request,redirect
import requests
from mongoCRUD import getPoster

app = Flask(__name__, template_folder="template")


@app.route('/')
def searchPoster():
    return '''<html>
    <body>
    <form action="search" method="POST">
    <label>Movie Name:</label>
    <input type="search" name="image">
    <input type="submit">
    </form>
    </body>
    </html>
    '''


@app.route('/search/<image>', methods=['GET', 'POST'])
def showPoster(image):
    #image = request.args.get('image')
    # search and upload to mongo function and show poster
    filename = getPoster(image)
    return f'''<html>
    <body>
    <form action="search">
    <label>Movie Name:</label>
    <input type="search" name="image">
    <input type="submit">
    </form>
    <img src="{filename}">
    </body>
    </html>
    '''


app.run(host='localhost',port=5000,debug=True)
