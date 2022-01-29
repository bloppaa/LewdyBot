import requests
import json

import embed as e


def get_random_danbooru_file():
    """
    Retorna la URL de un archivo aleatorio del board Danbooru.
    """
    url = 'https://danbooru.donmai.us/posts/random.json?tags=-rating:safe'
    response = requests.get(url)
    json_data = json.loads(response.text)

    # Si no se puede obtener el id del archivo, significa que no es visible.
    # En este caso, recurriremos a la recursion.
    file_id = json_data.get('id')

    if not file_id:
        return get_random_danbooru_file()
    else:
        # Si la extension del archivo es zip, la llave sera 'large_file_url',
        # ya que la extension de esa URL es webm.
        file_extension = json_data['file_ext']
        key = 'large_file_url' if file_extension == 'zip' else 'file_url'
        file_url = json_data[key]

        characters = json_data['tag_string_character']
        return file_url + '\n' + format_characters(characters)


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
