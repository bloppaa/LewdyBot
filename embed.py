import discord


def get_help_embed():
    """
    Retorna el embed que contiene la información de cómo funcionan
    los comandos del bot.
    """
    help_embed = discord.Embed(
        title='Lista de comandos',
        colour=0xab77a3,
        description=(
            '`$r34 <tag>` Muestra una imagen hentai aleatoria que contenga el tag.\n'
            '`$safe <tag>` Muestra una imagen SFW aleatoria que contenga el tag.'
            ),
    )
    return help_embed