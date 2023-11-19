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
    
    def get_all_domains(self):
        all_domains = self.clients_collection.distinct('domains')
        return all_domains

    def insert_new_api(self, api_name, api_key, bot_name, style, pfp, template, system_prompt, domains):
        api_document = {
            {
                "key_name": api_name,
                "api_key": api_key,
                "bot_name": bot_name,
                "widget": {
                    "style": style,
                    "pfp": pfp,
                    "template": template,
                },
                "system_prompt": system_prompt,
                "domains": domains
            }
        }

        self.clients_collection.insert_one(api_document)


if '__main__' == __name__:
    cb = ClientBase()
    key = generate_apikey()
    cb.insert_new_api("test key", key, bot_name="test2", style={
        "primary_color": "#0033cc",
        "background_color": "#f5f8ff"
    }, pfp="https://i.imgur.com/dsI355M.png", template='tmpl-1.html', system_prompt='', domains=["*"])
    print(cb.api_exists(key))
