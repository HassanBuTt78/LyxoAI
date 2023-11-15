import secrets

def generate_chatid():
    id = secrets.token_hex(15)
    return id

def generate_apikey():
    id = secrets.token_hex(32)
    return id