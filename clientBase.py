from pymongo import MongoClient
from bson import ObjectId
from config import DATABASE_URI
from utils import generate_apikey

class ClientBase:
    def __init__(self):
        self.client = MongoClient(DATABASE_URI)
        self.db = self.client['chatbot']
        self.clients_collection = self.db['clients']

    def api_exists(self, api_key):
        return bool(self.clients_collection.find_one({'api_key': api_key}))
    
    def get_user_info(self, user_id):
        return self.clients_collection.find_one({'_id': ObjectId(user_id)})
    
    def get_user_info_by_key(self, api_key):
        return self.clients_collection.find_one({'api_key': api_key})
    
    def insert_new_api(self, api_name, api_key):
        api_document = {
            'key_name': api_name,
            'api_key': api_key,
        }

        self.clients_collection.insert_one(api_document)


if '__main__' == __name__:
    cb = ClientBase()
    key = generate_apikey()
    cb.insert_new_api("test key", key)
    print(cb.api_exists(key))