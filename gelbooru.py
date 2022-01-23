import requests
import json


def get_random_r34_media():
    url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=sort:random+-rating:safe+score:>=10'
    response = requests.get(url)
    json_data = json.loads(response.text)

    post = json_data['post'][0]
    post_url = post['sample_url']
    if post_url:
        return post_url
    else:
        post_url = post['file_url']
        return post_url
