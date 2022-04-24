from pymongo import MongoClient
from gridfs import GridFS
from os import environ
import requests

HOST = environ.get('PROJ_MONGO_HOST', 'localhost')
PORT = int(environ.get('PROJ_MONGO_PORT', '27017'))
DB_POSTERS = environ.get('PROJ_MONGO_FILES_DB', 'posters')
DB_CACHE   = environ.get('PROJ_MONGO_CACHE_DB', 'cache')

class mongoConnection:

    def __init__(self, db=DB_CACHE, host=HOST, port=PORT):
        self.opts = {'host': host, 'port': port}
        self.database = db

    @property
    def db(self):
        return MongoClient(**self.opts)[self.database]


class cache(mongoConnection):

    def __init__(self, db=DB_CACHE):
        super().__init__(db)
        self.table = 'seen_ids'
        # if self.table not in self.db.list_collection_names():
        #     self.db.create_collection(self.table)
        #     self.db[self.table].create_index('id')

    def put(self, entries, name):
        for entry in entries:
            entry.update({"search": name})
            self.db[self.table].insert_one(entry)

    def search_by_name(self, name):
        return [* self.db[self.table].find({"search": name})]


class posterStorage(mongoConnection):

    def __init__(self, db=DB_CACHE):
        super().__init__(db)

    @property
    def files(self): return GridFS(self.db)

    def save(self, name, data):
        return self.files.put(data, filename=name)

    def find(self, name):
        return self.files.find_one({'filename': name})

    def overwrite(self, name, data):
        self.delete(name)
        self.save(name, data)

    def delete(self, name):
        return self.files.delete(self.find(name)._id)

if __name__ == "__main__":
    db = posterStorage()
    print(1)
    file = requests.get("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi0.wp.com%2Fwallpapershero.com%2Fwp-content%2Fuploads%2Fsites%2F13%2F2014%2F11%2FCat-Sad-Annoyed.jpg%3Ffit%3D2560%252C1600%26ssl%3D1&f=1&nofb=1")
    print(2)
    db.save(name='test', data=file.content)
    print(3)
    db.delete('test')
    print(4)
