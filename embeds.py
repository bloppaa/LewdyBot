import discord


def get_help_embed():
    """
    Retorna el embed que contiene la información de cómo funcionan
    los comandos del bot.
    """
    help_embed = discord.Embed(
        title='Lista de comandos',
        description='`$r34 <tag>` Muestra un archivo hentai aleatorio que contenga el tag. Si se omite el tag muestra un archivo cualquiera'
    )
    return help_embed