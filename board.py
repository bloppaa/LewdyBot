import requests
import json

import embed as e


def get_random_image_danbooru(tag=None, nsfw=True):
    """
    Retorna un archivo aleatorio obtenido de Danbooru con los personajes
    que se encuentran en él. Si se omite el tag, busca un archivo cualquiera.
    Por defecto busca archivos NSFW, pero también puede buscar imágenes safe.
    Si el archivo es una imagen, retorna un embed, sino sólo retorna un string.
    """
    # Sólo se buscan archivos con un score de 10 o más.
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

    # Obtiene el estado de la petición. 
    # Si fracasa, retorna un mensaje especificando el error.
    success = json_data.get('success')
    if success == False:
        messages = {
            'You cannot search for more than 2 tags at a time.':
            'No puedes buscar mas de 2 tags al mismo tiempo.',
            'That record was not found.': 'No se encontró ese tag.',
        }
        message = json_data['message']
        return messages.get(message, 'Error.')
    # Verifica que el archivo sea una imagen para retornar un embed.
    # Sino sólo regresa la URL del video.
    else:
        is_deleted = json_data['is_deleted']
        if is_deleted:
            get_random_image_danbooru(tag, nsfw)

        characters = format_characters(json_data['tag_string_character'])
        extension = json_data['file_ext']
        if extension == 'zip':
            return f"{json_data['file_url']}\n_**{characters}**_"
        if extension == 'mp4' or extension == 'webm':
            return f"{json_data['file_url']}\n_**{characters}**_"
        else:
            file_url = json_data.get('file_url', json_data['large_file_url'])
            embed = e.get_image_characters_embed(file_url, characters)
            return embed


def format_characters(characters):
    """
    Le da formato al string obtenido de la API de Danbooru que contiene
    a los personajes de la imagen.
    Formato: 'name_1 name_2' -> 'Name 1, Name 2'.
    """
    characters = characters.split()
    for i in range(len(characters)):
        characters[i] = ' '.join(characters[i].split('_'))

    characters_string = ', '.join(characters).title()
    return characters_string
