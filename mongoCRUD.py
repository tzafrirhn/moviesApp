from pymongo import MongoClient
from gridfs import GridFS
# import requests

PROJ_HOST = 'localhost'
PROJ_PORT = 27017
PROJ_DB   = "posters_database"

class posterStorage:

    def __init__(self, db, host, port):
        self.opts = {'host': host, 'port': port}
        self.database = db

    @property
    def files(self):
        connection = MongoClient(**self.opts)
        return GridFS(connection[self.database])

    def save(self, name, data):
        return self.files.put(data, filename=name)

    def find(self, name):
        return self.files.find_one({'filename': name})

    def overwrite(self, name, data):
        self.delete(name)
        self.save(name, data)

    def delete(self, name):
        return self.files.delete(self.find(name)._id)

# if __name__ == "__main__":
#     db = posterStorage(db=PROJ_DB, host=PROJ_HOST, port=PROJ_PORT)
#     file = requests.get("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi0.wp.com%2Fwallpapershero.com%2Fwp-content%2Fuploads%2Fsites%2F13%2F2014%2F11%2FCat-Sad-Annoyed.jpg%3Ffit%3D2560%252C1600%26ssl%3D1&f=1&nofb=1")
#     db.save(name='test', data=file.content)
#     db.delete('test')
