import requests
import json

import embed as e


def __get_random_danbooru_post(nsfw):
    """
    Retorna una publicacion aleatoria de Danbooru con la lista de
    personajes que aparecen en ella.
    """
    url = ('https://danbooru.donmai.us/posts/random.json?tags=order:rank'
           '+-status:deleted')
    if nsfw:
        url += '+-rating:safe'
    elif nsfw == False:
        url += '+rating:safe'
        
    response = requests.get(url)
    json_data = json.loads(response.text)

    file_id = json_data.get('id')
    # Si no se puede obtener el id de la publicacion, significa que no es visible.
    # En este caso, recurriremos a la recursion.
    if not file_id:
        return __get_random_danbooru_post(nsfw)
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


def get_rand_danbooru_file_by_tag(nsfw, tag=None):
    """
    Retorna una publicacion aleatoria de Danbooru con la lista de personajes que
    aparecen en él. Si se provee un tag, busca una publicacion que contenga ese
    tag. Si se omite, llama a _get_random_danbooru_post().
    """
    if not tag:
        return __get_random_danbooru_post(nsfw)
    else:
        tag = '_'.join(tag.split())
        
    url = ('https://danbooru.donmai.us/posts.json?tags=order:random+limit:3'
           f'+-status:deleted+{tag}')
    if nsfw:
        url += '+-rating:safe'
    elif nsfw == False:
        url += '+rating:safe'

    response = requests.get(url)
    json_data = json.loads(response.text)

    # Si la lista esta vacia, significa que el tag no existe.
    if not json_data:
        msg = '_**No existe ese tag**.'
        tag = __get_fuzzy_name_match_danbooru(tag)
        if tag:
            msg += f' ¿Quizá quisiste decir_ `{tag}`_?'
        return msg + '_'

    # Atrapa cualquier error que pueda surgir.
    try:
        success = json_data.get('success')
    except AttributeError:
        success = None
    if success == False:
        print(json_data['message'])
        error_msg = ('_No se pueden buscar múltiples tags con _`$db`_.'
                     ' Intenta usando _`$gb`.')
        return error_msg
    
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
        return '_**Sin resultados**. Intenta buscando otra cosa._'


def __get_fuzzy_name_match_danbooru(tag):
    '''
    Obtiene el tag parecido al tag original con más posts.
    '''
    url = ('https://danbooru.donmai.us/tags.json?search[order]=count'
           f'&search[fuzzy_name_matches]={tag}')
    response = requests.get(url)
    json_data = json.loads(response.text)

    if json_data:
        return json_data[0]['name']
    else:
        return None


def format_characters(characters):
    """
    Le da formato(*) al string que contiene a los personajes del archivo.
    (*)Formato: 'name_1 name_2' -> 'Name 1, Name 2'.
    """
    characters = characters.split()
    for i in range(len(characters)):
        characters[i] = ' '.join(characters[i].split('_'))

    characters_string = ', '.join(characters).title()
    return characters_string
