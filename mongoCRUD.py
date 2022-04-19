from pymongo import MongoClient
import gridfs

connection_url = "mongodb://localhost:27017/"
db_name = "posters_database"

# def createDB():
db = MongoClient(connection_url).gridfs_example
# Create an object of GridFs for the above database.
#database = connection[db_name]

def newPoster(file):
    # Create an object of GridFs for the above database.
    fs = gridfs.GridFS(db)
    # Open the image in read-only format.
    with open(file, 'rb') as f:
        contents = f.read()

    # Now store/put the image via GridFs object.
    fs.put(contents, filename="file")


def readPoster():
    pass

newPoster("https://dictionary.cambridge.org/fr/images/thumb/poster_noun_002_28550.jpg")