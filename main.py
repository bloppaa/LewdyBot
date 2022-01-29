import discord
import os

import board as b
import embed as e
from keep_alive import keep_alive

client = discord.Client(activity=discord.Game('$help'))


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

    # Verifica que el mensaje empiece con el prefijo '$' para
    # realizar las acciones del bot.
    if msg.startswith('$'):
        msg = msg[1:]
        words = msg.split(maxsplit=1)
        action = words[0]

        # Busca los argumentos del comando. 
        # Si no hay entonces tendrán el valor None.
        args = None
        try:
            args = words[1]
        except IndexError:
            pass

        if action == 'help' or action == 'h':
            embed_msg = e.get_help_embed()
            await message.channel.send(embed=embed_msg)
        
        elif action == 'danbooru' or action == 'db':
            url = b.get_random_danbooru_file()
            await message.channel.send(url)

        elif action == 'safe' or action == 's':
            image = b.get_random_image_danbooru(args, False)
            if isinstance(image, discord.Embed):
                await message.channel.send(embed=image)
            else:
                await message.channel.send(image)

keep_alive()
client.run(os.getenv('TOKEN'))
