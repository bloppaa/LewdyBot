import requests
import json


def get_random_file_url(tag=None, nsfw=True):
    """
    Retorna una URL de un archivo NSFW aleatorio obtenido de Danbooru.
    Si se omite el tag, regresa una URL de un archivo cualquiera.
    Por defecto busca archivos NSFW, pero puede cambiarse a SFW.
    """
    url = f'https://danbooru.donmai.us/posts/random.json?tags=+score:>=10'
    if nsfw:
        url += f'+-rating:safe'
    else:
        url += f'+rating:safe'

    if tag:
        words = tag.split()
        tag = '_'.join(words) # Une las palabras del tag con un guión bajo
        url += f'+{tag}'

    response = requests.get(url)
    json_data = json.loads(response.text)
    
    success = json_data.get('success')
    if success == False:
        messages = {
            'You cannot search for more than 2 tags at a time.': 'No puedes buscar mas de 2 tags al mismo tiempo.',
            'That record was not found.': 'No se encontró ese tag, ¿quizá lo escribiste mal?',
        }
        message = json_data['message']
        return messages[message]
    else:
        file_url = json_data['file_url']
        return file_url
