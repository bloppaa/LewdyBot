import discord


def get_help_embed():
    """
    Retorna un embed que contiene ayuda sobre los comandos del bot.
    """
    help_embed = discord.Embed(
        title='Lista de comandos',
        colour=0xab77a3,
        description=(
            '`$danbooru [tag]` | `$db [tag]`\nMuestra una imagen o video de '
            '[Danbooru](https://danbooru.donmai.us/).'
            ),
    )
    help_embed.set_footer(text='Sintaxis: <requerido> [opcional]')
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