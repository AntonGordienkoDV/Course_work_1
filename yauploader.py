import requests
import os
import json
from collections import Counter


class YaUploader:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, _token: str):
        self.token = _token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, parent_dir: str = '/', new_dir: str = ''):
        if new_dir == '':
            return parent_dir
        else:
            url = f'{self.host}/v1/disk/resources'
            headers = self.get_headers()
            if parent_dir == '/':
                new_folder_path = f'{parent_dir}{new_dir}'
            else:
                new_folder_path = f'{parent_dir}/{new_dir}'
            params = {'path': new_folder_path}
            response = requests.put(url, headers=headers, params=params)
            if response.status_code in [201, 409]:
                print(f'\nCreating folder {new_folder_path} -> OK\n')
        return new_folder_path

    def _get_upload_link(self, path):
        url = f'{self.host}/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('href')

    def upload_file(self, path, file_name):
        upload_link = self._get_upload_link(path)
        headers = self.get_headers()
        response = requests.put(upload_link, data=open(file_name, 'rb'), headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print(f'Uploading file {file_name} -> OK\n')

    def upload(self, file_path: str, upload_folder_path: str = ''):
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                print(f'Prepare file {file_path} to upload')
                upload_file_name = upload_folder_path + '/' + os.path.basename(file_path)
                self.upload_file(upload_file_name, file_path)
            elif os.path.isdir(file_path):
                upload_folder_path = self.create_folder(upload_folder_path, os.path.basename(file_path))
                files_list = os.listdir(file_path)
                for file_name in files_list:
                    self.upload(os.path.join(file_path, file_name), upload_folder_path)
        else:
            print(f'Error! File or directory {file_path} is not found')

    def get_vk_files_links_list(self, files_data_json_path):
        files_list = []
        with open(files_data_json_path, encoding='utf-8') as fd:
            files_data = json.load(fd)
        likes = Counter([photo['likes']['count'] for photo in files_data['items']])
        for photo in files_data['items']:
            photo_data = dict()
            photo_data['link'] = photo['sizes'][-1]['url']
            if likes[photo['likes']['count']] > 1:
                photo_data['name'] = f"{photo['likes']['count']}_{photo['date']}"
            else:
                photo_data['name'] = photo['likes']['count']
            files_list.append(photo_data)
        return files_list

    def get_folder_name(self, files_data_json_path):
        with open(files_data_json_path, encoding='utf-8') as fd:
            files_data = json.load(fd)
        return f'Фото_VK_{files_data["name"]}'

    def upload_remote_file(self, file_name: str, file_link: str, upload_folder: str = '/'):
        url = f'{self.host}/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {
            'path': f"{upload_folder}/{file_name}",
            'url': file_link
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 202:
            return
        else:
            print(f'Error {response.status_code}!')

    def upload_remote_files(self, files_data_json_path):
        new_folder_name = self.get_folder_name(files_data_json_path)
        upload_folder = self.create_folder(new_dir=new_folder_name)
        files_list = self.get_vk_files_links_list(files_data_json_path)
        print(f'Uploading files to {upload_folder}... Wait...\n')
        for item in files_list:
            print(f'Uploading file {item["name"]} from {item["link"]}')
            self.upload_remote_file(item['name'], item['link'], upload_folder)

