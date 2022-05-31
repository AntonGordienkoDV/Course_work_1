import requests
import time
import json
import os


class VKDownloader:
    host = 'https://api.vk.com/method/'

    def __init__(self, token: str, version: str, owner_id=None):
        self.params = {
            'owner_id': owner_id,
            'access_token': token,
            'v': version
        }

    def get_profile_info(self):
        url = self.host + 'users.get'
        user_data = requests.get(url, params=self.params).json()
        return user_data['response'][0]

    def make_photos_data_json(self, response_json):
        path = os.getcwd()
        if 'logs' not in os.listdir(path):
            path = os.path.join(path, 'logs')
            os.mkdir(path)
        else:
            path = os.path.join(path, 'logs')
        user_data = self.get_profile_info()
        if f'{user_data["id"]}_photos_data.json' in os.listdir(path):
            path = os.path.join(path, f'{user_data["id"]}_photos_data.json')
            with open(path, encoding='utf-8') as pd:
                photos_data = json.load(pd)
            photos_data['items'].extend(response_json['response']['items'])
            with open(path, 'w', encoding='utf-8') as pd:
                json.dump(photos_data, pd, ensure_ascii=False, indent=4)
        else:
            path = os.path.join(path, f'{user_data["id"]}_photos_data.json')
            with open(path, 'w', encoding='utf-8') as pd:
                data = response_json['response']
                data['name'] = f"{user_data['first_name']} {user_data['last_name']}"
                json.dump(data, pd, indent=4, ensure_ascii=False)
        return path

    def get_photos(self, album_id='profile'):
        url = self.host + 'photos.get'
        photos_geting_params = {
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 1,
            'offset': 0,
            'count': 1000
        }
        print('Get photos from VK... Wait...\n')
        while True:
            response = requests.get(url, params={**self.params, **photos_geting_params}).json()
            json_path = self.make_photos_data_json(response)
            if (response['response']['count'] - photos_geting_params['offset']) > photos_geting_params['count']:
                photos_geting_params['offset'] += photos_geting_params['count']
                print(f'Writing photos data into log... {photos_geting_params["offset"]} / \
{response["response"]["count"]}')
                time.sleep(0.33)
            else:
                print('\nSuccess!\n')
                return json_path
