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

    msg = message.content

    if msg.lower() == '$r34':
        url = h.get_random_r34_media()
        await message.channel.send(url)


keep_alive()
client.run(os.getenv('TOKEN'))
