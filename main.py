import discord
import os

import hentai as h

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.lower() == '$r34':
        url = h.get_random_r34_media()
        await message.channel.send(url)


client.run(os.environ['LEWDY_TOKEN'])
