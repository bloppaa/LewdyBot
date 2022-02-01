import discord


def get_help_embed():
    """
    Retorna un embed que contiene ayuda sobre los comandos del bot.
    """
    help_embed = discord.Embed(
        title='Lista de comandos',
        colour=0xab77a3,
        description=(
            'Detalle del comando: `$help <comando>`\n\n'
            '`$danbooru` : Muestra una imagen o video de '
            '[Danbooru](https://danbooru.donmai.us/).'
            ),
    )
    help_embed.set_footer(
        icon_url = ('https://cdn.discordapp.com/avatars/'
                    '874886185175097366/217166ec269838379e62ea3131cfadd0.webp'
                    '?size=128'),
        text='© Blopa',)
    return help_embed


def get_help_danbooru_embed():
    """
    """
    help_embed = discord.Embed(
        title='Comando gelbooru',
        colour=0xab77a3,
        description=(
            'Muestra una imagen o video de [Danbooru](https://danbooru.donmai.us/).'
            '\nUsa `/safe` o `/nsfw` para filtrar el contenido.'
            '\n\n**Uso**\n`!danbooru [tag][/modo]`'
            '\n\n**Alias comando**\n`!db`'
            '\n\n**Alias modos**\n`/s`\n`/n`'
        ),
    )
    help_embed.set_footer(
        text='Sintaxis <requerido> [opcional]',
    )
    return help_embed


def get_image_characters_embed(post_url, file_url, characters):
    """
    Retorna un embed con la imagen, el link al post original y el/los personajes
    que aparecen en ella.
    """
    db_embed = discord.Embed(
        colour=0xcd7f32,
        description=f'[Post original]({post_url})',
        )
    db_embed.set_image(url=file_url)
    db_embed.set_footer(text=characters)
    
    return db_embed