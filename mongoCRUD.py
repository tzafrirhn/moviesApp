import gridfs
import requests
import os
from pymongo import MongoClient

connection_url = "mongodb://localhost:27017/"


def mongoConnect():
    try:
        conn = MongoClient(connection_url)
        print("MongoDB connected", conn)
        return conn.PosterFiles
    except Exception as e:
        print("Error in Mongo Connection:", e)


def newPoster(file):
    db = mongoConnect()
    # Create an object of GridFs for the above database.
    fs = gridfs.GridFS(db)
    # Open the image in read-only format.
    if file.startswith('http://') or file.startswith('https://'):
        imContent = requests.get(file)
    else:
        with open(file, 'rb') as f:
            imContent = f.read()

    # Now store/put the image via GridFs object.
    name = file.split('/')
    print(name[-1])
    fs.put(imContent.content, filename=name[-1])


def getPoster(name):
    db = mongoConnect()
    fs = gridfs.GridFS(db)
    try:
        print(name)
        data = fs.find_one({'filename': name})
        image = data.read()
        temp = open("images/poster.jpg", 'wb')
        temp.write(image)
        path=os.path.join(os.path.abspath("."),"images","poster.jpg")
        temp.close()
    except Exception as e:
        print(e)
    return path


getPoster("pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg")
# newPoster("https://image.tmdb.org/t/p/original/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg")
