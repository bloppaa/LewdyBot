import discord
import os

import danbooru as d
import embed as e
from keep_alive import keep_alive

client = discord.Client(activity=discord.Game('$help'))


def get_media(words, nsfw=True):
    """
    Busca un tag en el mensaje que se envió hacia el bot. Retorna la URL del archivo que contiene
    ese tag, si es que lo encuentra, sino retorna un archivo aleatorio. El archivo puede ser o no
    ser NSFW, dependiendo del segundo parámetro.
    En caso de que el tag o el archivo no exista, retorna un mensaje informando esto.
    """
    tag = None
    try:
        tag = words[1]
    except IndexError:
        pass
            
    file_url = d.get_random_file_url(tag, nsfw)
    return file_url


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    # Previene que el bot se responda a sí mismo.
    if message.author == client.user:
        return

    # Previene que el bot responda en un canal de mensajes directos.
    if isinstance(message.channel, discord.DMChannel):
        return

    msg = message.content.lower()

    # Verifica que el mensaje empiece con el prefijo '$' para realizar las acciones del bot.
    if msg.startswith('$'):
        msg = msg[1:]
        words = msg.split(maxsplit=1)
        action = words[0]

        if action == 'help':
            embed_msg = e.get_help_embed()
            await message.channel.send(embed=embed_msg)
        
        elif action == 'r34':
            await message.channel.send(get_media(words))

        elif action == 'safe':
            await message.channel.send(get_media(words, False))


keep_alive()
client.run(os.getenv('TOKEN'))
