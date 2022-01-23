import discord
import os

import hentai as h
from keep_alive import keep_alive

client = discord.Client()


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
        words = msg.split()
        action = words[0]

        if action == 'help':
            pass
        
        elif action == 'r34':
            tag = None
            try:
                tag = words[1]
            except IndexError:
                pass
            finally:
                file_url = h.get_random_r34(tag)
                await message.channel.send(file_url)

        elif action == 'safe':
            pass


keep_alive()
client.run(os.getenv('TOKEN'))
