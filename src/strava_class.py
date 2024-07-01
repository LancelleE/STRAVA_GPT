import requests
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dotenv import set_key

# Handle authentication and token refresh
class StravaAuth:
    """
    ...
    """
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, access_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def refresh_access_token(self) -> str:
        """
        ...
        """
        # Implementation of token refresh
        # Updates self.access_token and returns it
        # url = f"https://www.strava.com/api/v3/oauth/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=refresh_token&refresh_token={self.refresh_token}"
        url = "https://www.strava.com/api/v3/oauth/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        response = requests.post(url, data=data, timeout=20).json()
        set_key(dotenv_path='.env',key_to_set= 'CLIENT_ACCESS_TOKEN', value_to_set=response['access_token'], quote_mode='never')
        self.access_token = response['access_token']

# Tool to make API calls
class StravaAPI:
    """
    ...
    """
    BASE_URL = "https://www.strava.com/api/v3/"

    def __init__(self, auth: StravaAuth):
        self.auth = auth

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None
        ) -> Dict:
        """
        ...
        """
        headers = {'Authorization': f'Bearer {self.auth.access_token}'}
        url = f"{self.BASE_URL}{endpoint}"
        # Implementation of API request
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, params=params, timeout=20)
            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, json=data, timeout=20)
            elif method.lower() == 'put':
                response = requests.put(url, headers=headers, json=data, timeout=20)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return {}

class ConfigManager:
    def __init__(self, config_file_path: str):
        self.config = self._load_config(config_file_path)

    def _load_config(self, config_file_path: str) -> dict:
        with open(config_file_path, 'r') as file:
            data = json.load(file)
        return data

    def get_config_for_activity_type(self, activity_type: str) -> dict:
        for config in self.config:
            if config['activity_type'] == activity_type:
                return config
        return None


# Deal with activities
class ActivityManager:
    """
    ...
    """
    def __init__(self, api: StravaAPI):
        self.api = api

    def get_latest_activities(self, after_date: str) -> List[int]:
        """
        ...
        """
        params = {'after': after_date, 'per_page': 200}
        response = self.api.make_request('get', "athlete/activities", params=params)
        return [act['id'] for act in response]

    def get_activity_data(self, activity_id: int) -> Dict:
        """
        ...
        """
        return self.api.make_request('get', f'activities/{activity_id}')

    def update_activity(self, activity_id: int, updates: Dict) -> None:
        """
        ...
        """
        self.api.make_request('put', f'activities/{activity_id}', data=updates)

class ProfileManager:
    """
    ...
    """
    def __init__(self, api: StravaAPI):
        self.api = api

    def get_profile_information(self) -> Dict:
        """
        ...
        """
        return self.api.make_request('get', "athlete")

class TitleTransformer:
    """
    ...
    """
    # Load the right config for my activity
    def __init__(self, config_file_path: str):
        self.config_manager = ConfigManager(config_file_path)

    def _find_matching_transformation(self, transformations: list, activity_date: datetime) -> dict:
        # This method finds a matching transformation based on the activity date
        for transform in transformations:
            event_date = datetime.strptime(transform['event_date'], '%Y-%m-%d')
            days_before = timedelta(days=transform['days_before'])
            if event_date - days_before <= activity_date <= event_date:
                return transform
        return None
    
    def transform_title(self, activity: dict) -> str:
        """
        ...
        """
        activity_type = activity['type']
        activity_date = datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ')
        
        config = self.config_manager.get_config_for_activity_type(activity_type)
        if not config:
            return activity['name']
        
        transform = self._find_matching_transformation(config['transformations'], activity_date)
        
        new_title_parts = []
        title = ''

        if transform:
            days_to_event = (datetime.strptime(transform['event_date'], '%Y-%m-%d') - activity_date).days
            new_title_parts.append(f"[{transform['emoji']}")
            title += f"[{transform['emoji']}"
            if transform['nickname']:
                new_title_parts.append(f"{transform['nickname']}")
                title += f" {transform['nickname']}"
                
            if days_to_event > 0:
                new_title_parts.append(f"(J-{days_to_event})")
                title += f" (J-{days_to_event})"
            
            title += f"] {activity['name']}"

            new_title_parts.append(']')
                
            # if days_to_event > 0:
            #     new_title_parts.append(f"(J-{days_to_event})")

        new_title_parts.append(activity['name'])

        # return "".join(new_title_parts)
        return title


class StravaManager:
    """
    ...
    """
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, access_token: str, min_date: str, config_file_path: str):
        """
        ...
        """
        auth = StravaAuth(client_id, client_secret, refresh_token, access_token)
        api = StravaAPI(auth)
        self.activity_manager = ActivityManager(api)
        self.profile_manager = ProfileManager(api)
        self.title_transformer = TitleTransformer(config_file_path)
        self.min_date = min_date

    def process_latest_activities(self):
        """
        ...
        """
        activities = self.activity_manager.get_latest_activities(self.min_date)
        for activity_id in activities:
            activity_data = self.activity_manager.get_activity_data(activity_id)
            new_title = self.title_transformer.transform_title(activity_data)
            if new_title != activity_data['name']:
                self.activity_manager.update_activity(activity_id, {'name': new_title})

    def get_profile_info(self):
        """
        ...
        """
        return self.profile_manager.get_profile_information()
