import threading
import requests
from src.config import CLIENT_ID, CLIENT_SECRET
from src.flask_app import run_flask_app, auth_data
from src.auth import get_authorization_code, exchange_authorization_code_for_tokens, wait_for_authorization_code

def main():
    threading.Thread(target=run_flask_app).start()
    get_authorization_code(CLIENT_ID)
    authorization_code = wait_for_authorization_code()
    
    print(f"Authorization code: {authorization_code}")
    
    token_info = exchange_authorization_code_for_tokens(CLIENT_ID, CLIENT_SECRET, authorization_code)
    
    print(f"Access token: {token_info['access_token']}")
    print(f"Refresh token: {token_info['refresh_token']}")

    activities_url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': f'Bearer {token_info['access_token']}'}
        
    response = requests.get(activities_url, headers=headers)
    print(response.json()[0])

if __name__ == '__main__':
    main()

    