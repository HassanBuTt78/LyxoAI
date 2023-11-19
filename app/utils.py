import secrets


def generate_chatid():
    id = secrets.token_hex(15)
    return id


def generate_apikey():
    id = secrets.token_hex(32)
    return id


def is_valid_host(host, allowed_hosts):
    if host == None:
        return '*' in allowed_hosts
    return host in allowed_hosts or '*' in allowed_hosts


def authenticate_request(request, cb):
    if 'Authorization' not in request.headers:
        return {'error': 'Authentication Error - API key not provided', 'authorized': False}
    authorization_header = request.headers['Authorization']
    _, api_key = authorization_header.split(' ')
    client_info = cb.get_user_info_by_key(api_key)
    if not client_info:
        return {'error': 'Authentication Error - Invalid API key provided', 'authorized': False}
    return {'authorized': True, 'system_prompt': client_info['system_prompt']}