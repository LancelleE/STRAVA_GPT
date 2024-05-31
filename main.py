import threading
import requests
from src.config import CLIENT_ID, CLIENT_SECRET
from src.flask_app import run_flask_app, auth_data
from src.auth import get_authorization_code, exchange_authorization_code_for_tokens, wait_for_authorization_code
from src.strava import Strava

def main():
    # Get the first authorization code
    threading.Thread(target=run_flask_app).start()
    get_authorization_code(CLIENT_ID)
    authorization_code = wait_for_authorization_code()
    token_info = exchange_authorization_code_for_tokens(CLIENT_ID, CLIENT_SECRET, authorization_code)
    print(token_info['access_token'])
    # Initiates the Strava instance
    strava = Strava(access_token=token_info['access_token'])
    print(strava)
    
    new_data = {
        "description": "Test de l'API de Strava !"
    }
    strava.update_activity(id_activity='11511427976', update=new_data)
    
    

if __name__ == '__main__':
    main()

    