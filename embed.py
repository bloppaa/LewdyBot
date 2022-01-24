import discord


def get_help_embed():
    """
    Retorna un embed que contiene ayuda sobre los comandos del bot.
    """
    help_embed = discord.Embed(
        title='Lista de comandos',
        colour=0xab77a3,
        description=(
            '`$danbooru <tag>` / `$db <tag>`\nMuestra una imagen NSFW de Danbooru.\n'
            '\n`$safe <tag>` / `$s <tag>`\nMuestra una imagen SFW de Danbooru.'
            ),
    )
    return help_embed


def format_characters(characters):
    """
    Le da formato al string obtenido de la API de Danbooru que contiene a los personajes de la imagen.
    Formato: 'name_1 name_2' -> 'Name 1, Name 2'.
    """
    characters = characters.split()
    for i in range(len(characters)):
        characters[i] = ' '.join(characters[i].split('_'))

    characters_string = ', '.join(characters).title()
    return characters_string


def get_danbooru_embed(file_url, characters):
    """
    Retorna un embed con la imagen y el/los personajes que aparecen en ella.
    """
    db_embed = discord.Embed(colour=0xcd7f32)
    db_embed.set_image(url=file_url)
    db_embed.set_footer(text=format_characters(characters))
    
    return db_embed