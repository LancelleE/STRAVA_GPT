import threading
import requests
from datetime import datetime
from dotenv import set_key
from src.config import CLIENT_ID, CLIENT_SECRET, CLIENT_REFRESH_TOKEN, CLIENT_ACCESS_TOKEN, LATEST_RUN
from src.flask_app import run_flask_app, auth_data
from src.auth import get_authorization_code, exchange_authorization_code_for_tokens, wait_for_authorization_code
from src.strava import Strava

def main():
    # Get the first authorization code
    threading.Thread(target=run_flask_app).start()
    get_authorization_code(CLIENT_ID)
    authorization_code = wait_for_authorization_code()
    token_info = exchange_authorization_code_for_tokens(CLIENT_ID, CLIENT_SECRET, authorization_code)
    set_key('.env', 'CLIENT_ACCESS_TOKEN', token_info['access_token'])
    print(token_info['access_token'])
    
    # Load logs and get the latest run, to update min_date
    # TODO
    
    # Initiates the Strava instance
    strava = Strava(
        strava_tokens= {
            'CLIENT_ID' : CLIENT_ID,
            'CLIENT_SECRET' : CLIENT_SECRET,
            'CLIENT_REFRESH_TOKEN' : CLIENT_REFRESH_TOKEN,
            'CLIENT_ACCESS_TOKEN' : CLIENT_ACCESS_TOKEN
        }, 
        min_date=LATEST_RUN
    )
    # Overwrite the LATEST_RUN in the .env file
    set_key(dotenv_path='.env',key_to_set= 'LATEST_RUN', value_to_set=str(datetime.now().timestamp()), quote_mode='never')

    # Check du ACCESS_TOKEN : si le temps restant < 1h, alors changer la clé et écrire dans le .env
    strava._refresh_access_token()
    
    # Scanner des nouvelles activités, depuis le dernier Run -> ça implique qu'à chaque Run, on note le timestamp à partir duquel il faut comparer ! Stocker où ?
    latest_activities = strava._get_latest_activities()
    if latest_activities:
        for id in latest_activities:
            strava.transform_title(id)
    else:
        print('No activity found !')
           
        
    
    # Pour chaque nouvelle activité détectée
    # TODO
    
    # En fonction du type d'activité, paramétrage particulier
    # TODO
    
    # Logs à saisir
    # TODO
    
    

if __name__ == '__main__':
    main()

    