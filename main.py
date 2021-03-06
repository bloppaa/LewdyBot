import discord
import os

import booru as b
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
        if len(words) > 1:
            args = words[1]
        else:
            args = None

        if action == 'help' or action == 'h':
            if args:
                if args == 'danbooru' or args == 'db':
                    embed_msg = e.get_help_danbooru_embed()
                    await message.channel.send(embed=embed_msg)
            # Embed de help general.
            else:
                embed_msg = e.get_help_embed()
                await message.channel.send(embed=embed_msg)
        
        elif action == 'danbooru' or action == 'db':
            # Verifica que se haya pasado un tag.
            nsfw = None
            if args:
                # Busca si se especifico un modo de busqueda.
                args = args.split('/')
                if len(args) > 1:
                    mode = args[1]
                    if mode == 'safe' or mode == 's':
                        nsfw = False
                    elif mode == 'nsfw' or mode == 'n':
                        nsfw = True
                    else:
                        error_msg = '_Modo inválido. Usa_ `/s` _o_ `/n`.'
                        await message.channel.send(error_msg)

            file = b.get_rand_danbooru_file_by_tag(nsfw, args[0] if args else None)
            if isinstance(file, discord.Embed):
                await message.channel.send(embed=file)
            else:
                await message.channel.send(file)
                
keep_alive()
client.run(os.getenv('TOKEN'))
