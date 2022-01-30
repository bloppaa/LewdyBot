import requests
import json

import embed as e


def get_random_danbooru_file():
    """
    Retorna un archivo NSFW aleatorio de Danbooru con la lista de personajes
    que aparecen en él.
    """
    url = 'https://danbooru.donmai.us/posts/random.json?tags=-rating:safe'
    response = requests.get(url)
    json_data = json.loads(response.text)

    file_id = json_data.get('id')
    # Si no se puede obtener el id del archivo, significa que no es visible.
    # En este caso, recurriremos a la recursion.
    if not file_id:
        return get_random_danbooru_file()
    else:
        # Si la extension del archivo es zip, entonces la llave sera
        # 'large_file_url'; de esta manera se obtendra un archivo webm.
        file_ext = json_data['file_ext']
        key = 'large_file_url' if file_ext == 'zip' else 'file_url'

        file_url = json_data[key]
        post_url = f'https://danbooru.donmai.us/posts/{file_id}'
        characters = format_characters(json_data['tag_string_character'])

        # Si el archivo es una imagen retorna una instancia de Embed.
        # Si el archivo es un video retorna un string con la informacion.
        if file_ext == 'zip' or file_ext == 'mp4' or file_ext == 'webm':
            info = (f'**Personajes**: {characters}\n'
                    f'**Video**: {file_url}')
            return info
        else:
            return e.get_image_characters_embed(post_url, file_url, characters)


def format_characters(characters):
    """
    Le da formato(*) al string obtenido de la API de Danbooru que contiene a los
    personajes del archivo.
    (*)Formato: 'name_1 name_2' -> 'Name 1, Name 2'.
    """
    characters = characters.split()
    for i in range(len(characters)):
        characters[i] = ' '.join(characters[i].split('_'))

    characters_string = ', '.join(characters).title()
    return characters_string
