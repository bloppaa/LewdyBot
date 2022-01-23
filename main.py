import discord
import os

import gelbooru as gb

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '$r34':
        media = gb.get_random_r34_media()
        await message.channel.send(media)


client.run(os.environ['LEWDY_TOKEN'])
