from pymongo import MongoClient


if __name__ == "__main__":
    c = MongoClient('localhost', 27017, directConnection=True)
    config = {'_id': 'services_set', 'members': [
    {'_id': 0, 'host': 'localhost:27017'},
    {'_id': 1, 'host': 'localhost:28017'},
    {'_id': 2, 'host': 'localhost:29017'}]}
    c.admin.command("replSetInitiate", config)
    c.close()
