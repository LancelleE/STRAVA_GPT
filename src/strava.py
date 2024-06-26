import requests
from geopy.geocoders import Nominatim
from dotenv import set_key

# Various functions, useful in the Strava class
def get_city_from_long_lat(latitude, longitude):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    city = address.get('city', '')
    return city

def mps_to_minspeed(speed_mps):
    # Conversion de m/s en km/min
    speed_kmpm = speed_mps * 60 / 1000  # Convertir m/s en km/min
    if speed_kmpm != 0:
        time_per_km = 1 / speed_kmpm  # Temps par kilomètre en minutes
        minutes = int(time_per_km)  # Partie entière représente les minutes
        seconds = (time_per_km - minutes) * 60  # Convertir la partie décimale en secondes
    else:
        minutes = float('inf')
        seconds = float('inf')
    return str(minutes) + ',' + str(round(seconds))

def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    time_str = ""
    if days > 0:
        time_str += f"{days} day(s), "
    if hours > 0:
        time_str += f"{hours} hour(s), "
    if minutes > 0:
        time_str += f"{minutes} minute(s) "
    if seconds > 0:
        time_str += f"and {seconds} second(s)"
    if days == 0 and hours == 0:
        time_str = f"{minutes} minute(s) et {seconds} second(s)"
    
    return time_str

class Strava:
    def __init__(self, strava_tokens: dict, min_date):
        # API IDs
        # self.access_token = access_token
        # self.client_id = client_id
        # self.client_secret = client_secret
        # self.client_refresh = client_refresh
        
        self.strava_tokens = strava_tokens
        
        
        self.base_url = "https://www.strava.com/api/v3/"
        self.headers = {'Authorization': f'Bearer {strava_tokens['CLIENT_ACCESS_TOKEN']}'}
        self.min_date = min_date
    
    def _refresh_access_token(self):
        # toutes les heures, faire la requête de refresh, puis regarder le remaining time.
        # Si le remaining time est inférieur à 1h, alors faire la bascule
        # Update le .env en ajoutant le nouveau .env
        url = f"{self.base_url}/oauth/token?client_id={self.strava_tokens['CLIENT_ID']}&client_secret={self.strava_tokens['CLIENT_SECRET']}&grant_type=refresh_token&refresh_token={self.strava_tokens['CLIENT_REFRESH_TOKEN']}"
        response = requests.post(url=url, headers=self.headers).json()
        if response['expires_in'] < 3600:
            set_key('../.env', 'CLIENT_ACCESS_TOKEN', response['access_token'])
            print('New CLIENT_ACCESS_TOKEN written !')
            print(f'New CLIENT_ACCESS_TOKEN written ! ! It remains {response['expires_in'] / 3600} hours.')
        else:
            print(f'No need to update CLIENT_ACCESS_TOKEN ! It remains {seconds_to_time(response['expires_in'])}.')
            
        pass
    
    def store_access_token():
        pass
        
        
    def __repr__(self) -> str:
        profile = self._get_profile_information()
        return f"Currently logged on {profile['firstname']} {profile['lastname']} profile."

    def _get_profile_information(self):
        url = self.base_url + "athlete"
        response = requests.get(url=url, headers=self.headers).json()
        return response
    
    def _get_latest_activities(self):
        url = f"https://www.strava.com/api/v3/athlete/activities?after={self.min_date}&per_page=200"
        response = requests.get(url=url, headers=self.headers).json()
        list_of_activities = []
        for act in response:
            list_of_activities.append((act['id']))
            
        return list_of_activities
    
    def get_activity_data(self, id_activity):
        url = f'{self.base_url}/activities/{id_activity}?include_all_efforts=False'
        response = requests.get(url=url, headers=self.headers).json()
        return response
    
    def _select_transform_fields(self, id_activity):
        activity = self.get_activity_data(id_activity=id_activity)
        output = {
            'nom' : activity['name'],
            'description' : activity['description'],
            'date' : activity['start_date_local'],
            'distance' : f'{activity['distance']/1000 : .2f} km',
            'temps_actif' : seconds_to_time(activity['moving_time']),
            'temps_total' : seconds_to_time(activity['elapsed_time']),
            'type' : activity['type'],
            'sport_type' : activity['sport_type'],
            'ville_depart' : get_city_from_long_lat(latitude=activity['start_latlng'][0], longitude=activity['start_latlng'][1]),
            'ville_fin' : get_city_from_long_lat(latitude=activity['end_latlng'][0], longitude=activity['end_latlng'][1]),
            'allure_moyenne' : mps_to_minspeed(activity['average_speed']) + " mn/km",
            'allure_maximale' : mps_to_minspeed(activity['max_speed']) + " mn/km",
            'deniv_max': activity['elev_high'],
            'deniv_min': activity['elev_low'],
            'deniv_positif' : round(activity['total_elevation_gain'],0),
            'calories' : round(activity['calories'])
        }
        
        for key, value in output.items():
            print(f'{key} : {value}')
        
    def update_activity(self, id_activity, update):
        url =  f"{self.base_url}activities/{id_activity}"
        response = requests.put(url, json=update, headers=self.headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            print("Activity updated successfully.")
        else:
            print("Failed to update activity.")
