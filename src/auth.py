import threading
import webbrowser
import requests
from .flask_app import auth_data

def get_authorization_code(client_id):
    authorization_url = (
        f"http://www.strava.com/oauth/authorize?client_id={client_id}"
        "&response_type=code&redirect_uri=http://localhost:8000/exchange_token"
        "&approval_prompt=force&scope=read_all,profile:read_all,activity:read_all,activity:write"
    )
    webbrowser.open(authorization_url)

def exchange_authorization_code_for_tokens(client_id, client_secret, authorization_code):
    token_url = 'https://www.strava.com/oauth/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()

def wait_for_authorization_code():
    while auth_data["authorization_code"] is None:
        threading.Event().wait(0.1)  # Wait for a short time to avoid busy waiting
    return auth_data["authorization_code"]
