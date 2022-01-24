import requests
import json

import embed as e


def get_random_image_danbooru(tag=None, nsfw=True):
    """
    Retorna un embed con una imagen aleatoria obtenido de Danbooru.
    Si se omite el tag, busca una imagen cualquiera. Por defecto busca imágenes
    NSFW, pero también puede buscar imágenes safe.
    """
    # Sólo se buscan imágenes con un score de 10 o más.
    url = f'https://danbooru.donmai.us/posts/random.json?tags=score:>=10'
    if nsfw:
        url += f'+-rating:safe'
    else:
        url += f'+rating:safe'

    # Si se entrega un tag, une las palabras con un guión bajo.
    if tag:
        words = tag.split()
        tag = '_'.join(words)
        url += f'+{tag}'

    response = requests.get(url)
    json_data = json.loads(response.text)

    # Obtiene el estado de la petición. Si fracasa, retorna un mensaje especificando el error.
    success = json_data.get('success')
    if success == False:
        messages = {
            'You cannot search for more than 2 tags at a time.': 'No puedes buscar mas de 2 tags al mismo tiempo.',
            'That record was not found.': 'No se encontró ese tag.',
        }
        message = json_data['message']
        return messages.get(message, 'Error.')
    # Verifica que el archivo sea una imagen. En caso contrario se hace recursión.
    else:
        extension = json_data['file_ext']
        if extension == 'mp4' or extension == 'webm':
            get_random_image_danbooru(tag, nsfw)
        
        file_url = json_data.get('file_url')
        if not file_url:
            return 'Ha ocurrido un error. Intenta de nuevo.'
            
        characters = json_data['tag_string_character']
        embed = e.get_danbooru_embed(file_url, characters)
        return embed
