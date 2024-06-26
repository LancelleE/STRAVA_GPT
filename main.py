import threading
import requests
from src.config import CLIENT_ID, CLIENT_SECRET, CLIENT_REFRESH_TOKEN, CLIENT_ACCESS_TOKEN
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
    strava = Strava(
        strava_tokens= {
            'CLIENT_ID' : CLIENT_ID,
            'CLIENT_SECRET' : CLIENT_SECRET,
            'CLIENT_REFRESH_TOKEN' : CLIENT_REFRESH_TOKEN,
            'CLIENT_ACCESS_TOKEN' : CLIENT_ACCESS_TOKEN
        }, 
        min_date=1716677003
    )
    print(strava)
    # Check du ACCESS_TOKEN : si le temps restant < 1h, alors changer la clé et écrire dans le .env
    strava._refresh_access_token()
    
    # Scanner des nouvelles activités, depuis le dernier Run -> ça implique qu'à chaque Run, on note le timestamp à partir duquel il faut comparer ! Stocker où ?
    # TODO
    
    # Pour chaque nouvelle activité détectée
    # TODO
    
    # En fonction du type d'activité, paramétrage particulier
    # TODO
    
    # Logs à saisir
    # TODO
    
    new_data = {
        "description": "Test de l'API de Strava !",
        "name": "Test"
    }
    strava.update_activity(id_activity='11511427976', update=new_data)
    
    

if __name__ == '__main__':
    main()

    