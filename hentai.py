import requests
import json


def get_random_r34_media():
    url = 'https://danbooru.donmai.us/posts/random.json'
    response = requests.get(url)
    json_data = json.loads(response.text)

    post_url = json_data['file_url']
    return post_url
