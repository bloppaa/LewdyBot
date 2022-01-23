import requests
import json


def get_random_r34(tag=None):
    url = f'https://danbooru.donmai.us/posts/random.json?tags=-rating:safe'
    if tag:
        url += f'+{tag}'
    response = requests.get(url)
    json_data = json.loads(response.text)

    post_url = json_data['file_url']
    return post_url
