import requests
import os
import json
from tqdm import tqdm

class Dowlander:
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.TOKENVK = 'vk1.a.lXzUJW1zi3eLHK_apXO8UwBTSYa--n7eoQ9i4Y97xM64gd1pZMu1VHkVKSn0QA4PW1l4GvP-dwtKxC0yII21' \
                       'PVOQX78Bm-JgtIADO_KvmW8CyqVuvtgss9Xr-zDqMGSy6_NhU-JX_2qs01CQJh3L2Iy33kiy_tlu0aKMj7wF40FzNLz' \
                       'yfPhEGTz_-H6_jCt4TyRI_qn4UBVegEBgptv0BQ'

    def get_common_params(self):
        return {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'access_token': self.TOKENVK,
            'v': '5.131',
            'extended': '1',
            'photo_sizes': '1'
        }

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = self.get_common_params()
        respons = requests.get(url=url, params=params)
        return respons.json()

    def get_all_photos(self):
        data = self.get_photos()
        max_size_photos = {}
        photo_information = []
        for photos in data['response']['items']:
            max_size = 0
            photo_info = {}
            for size in photos['sizes']:
                if size['height'] >= max_size:
                    max_size = size['height']
            for url in photos['sizes']:
                if url['height'] == max_size:
                    if photos['likes']['count'] not in max_size_photos.keys():
                        max_size_photos[photos['likes']['count']] = url['url']
                        photo_info['file_name'] = f"{photos['likes']['count']}.jpg"
                        photo_info['size'] = url['type']
                    else:
                        max_size_photos[f"{photos['likes']['count']}+{photos['date']}"] = url['url']
                        photo_info['file_name'] = f"{photos['likes']['count']}+{photos['date']}.jpg"
                        photo_info['size'] = url['type']

            photo_information.append(photo_info)
        with open('photo_info.json', 'w') as f:
            json.dump(photo_information, f, ensure_ascii=False, indent=2)
        return max_size_photos

    def new_folder(self):
        name_folder = 'Images_VK'
        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        params = {"path": name_folder}
        headers = {'Authorization': "OAuth " + token}
        response_2 = requests.put(url, headers=headers, params=params)
        return name_folder

    def post_photos(self):
        data = self.get_all_photos()
        new_folder = self.new_folder()
        for key in tqdm(data):
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            params = {"path": f'{new_folder}/{key}.jpg', "url":data[key]}
            headers = {'Authorization': "OAuth " + token}
            response = requests.post(url=url, headers=headers, params=params)


if __name__ == '__main__':
    user_id = int(input('Введите ваш VK_ID: '))
    token = str(input('Введите ваш токен Яндекс Диска: '))
    vk_client = Dowlander(token, user_id)
    result = vk_client.post_photos()
