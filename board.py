import requests
import json

import embed as e


def __get_random_danbooru_file():
    """
    Retorna un archivo NSFW aleatorio de Danbooru con la lista de personajes que
    aparecen en él.
    """
    url = 'https://danbooru.donmai.us/posts/random.json?tags=order:rank+-rating:safe'
    response = requests.get(url)
    json_data = json.loads(response.text)

    file_id = json_data.get('id')
    # Si no se puede obtener el id del archivo, significa que no es visible.
    # En este caso, recurriremos a la recursion.
    if not file_id:
        return __get_random_danbooru_file()
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
            info = (f'**Post original**: <{post_url}>\n'
                    f'**Personajes**: {characters}\n'
                    f'**Video**: {file_url}')
            return info
        else:
            return e.get_image_characters_embed(post_url, file_url, characters)


def get_random_danbooru_file_by_tag(tag=None):
    """
    Retorna un archivo aleatorio de Danbooru con la lista de personajes que 
    aparecen en él. Si se provee un tag, busca un archivo que contenga ese tag.
    Si se omite, llama a _get_random_danbooru_file().
    """
    if not tag:
        return __get_random_danbooru_file()
    else:
        tag = '_'.join(tag.split())
        
    url = f'https://danbooru.donmai.us/posts.json?tags=order:random+limit:3+{tag}'
    response = requests.get(url)
    json_data = json.loads(response.text)

    # Verifica que se haya pasado un tag valido.
    try:
        success = json_data.get('success')
    except AttributeError:
        success = True

    if success == False:
        return '**Sin resultados**. Intenta buscando otra cosa.'
    
    found = False  # Flag para verificar que encontro un post.
    for i in range(len(json_data)):
        # La logica es un poco distinta que de la funcion hermana, por eso se
        # requiere una funcion aparte.
        file_id = json_data[i].get('id')
        if not file_id:
            continue
        else:
            found = True
            file_ext = json_data[i]['file_ext']
            key = 'large_file_url' if file_ext == 'zip' else 'file_url'

            file_url = json_data[i][key]
            post_url = f'https://danbooru.donmai.us/posts/{file_id}'
            characters = format_characters(json_data[i]['tag_string_character'])  

            if file_ext == 'zip' or file_ext == 'mp4' or file_ext == 'webm':
                info = (f'**Post original**: <{post_url}>\n'
                        f'**Personajes**: {characters}\n'
                        f'**Video**: {file_url}')
                return info
            else:
                return e.get_image_characters_embed(post_url, file_url, characters)

    # Si no encontro ninguna imagen, se muestre un mensaje explicando el error.
    if not found:
        return '**Sin resultados**. Intenta buscando otra cosa.'


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
