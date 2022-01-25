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
    url = f'https://danbooru.donmai.us/posts/random.json?tags='
    if nsfw:
        url += f'+-rating:safe'
    else:
        url += f'+rating:safe'

    # Transforma el tag en el formato requerido por la API.
    if tag:
        tags = tag.split('+')
        for i in range(len(tags)):
            tags[i] = join_tag(tags[i])
        tag = '+'.join(tags)
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
            'That record was not found.': 'No se encontró ningún registro.',
        }
        message = json_data['message']
        return messages.get(message, 'Error.')
    # Verifica que el archivo sea una imagen para retornar un embed.
    # Sino sólo regresa la URL del video.
    else:
        # Si la imagen se eliminó, se recurre a la recursión.
        is_deleted = json_data['is_deleted']
        if is_deleted:
            get_random_image_danbooru(tag, nsfw)

        characters = format_characters(json_data['tag_string_character'])
        extension = json_data['file_ext']
        if extension == 'zip':
            message = f"{json_data['large_file_url']}"
            if characters:
                message += f'\n_**{characters}**_'
            return message

        if extension == 'mp4' or extension == 'webm':
            message = f"{json_data.get('file_url', json_data['large_file_url'])}"
            if characters:
                message += f'\n_**{characters}**_'
            return message

        else:
            try:
                file_url = json_data.get('file_url', json_data['large_file_url'])
            except KeyError:
                return 'Algo salió mal. Intenta otra cosa.'
            embed = e.get_image_characters_embed(file_url, characters)
            return embed


def join_tag(tag):
    """
    Une las palabras del tag con un guión bajo.
    """
    words = tag.split()
    tag = '_'.join(words)
    return tag


def format_characters(characters):
    """
    Le da el formato(*) al string obtenido de la API de Danbooru que contiene
    a los personajes del archivo.
    (*)Formato: 'name_1 name_2' -> 'Name 1, Name 2'.
    """
    characters = characters.split()
    for i in range(len(characters)):
        characters[i] = ' '.join(characters[i].split('_'))

    characters_string = ', '.join(characters).title()
    return characters_string
