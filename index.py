import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.shard import EventItem

import wavelinkcord as wavelink
import asyncio
import websockets
import subprocess
import sqlite3
import random
import ssl
import opustools

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"Готово! {bot.user} онлайн!")
    bot.loop.create_task(on_node())

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
   print(f"Node {node.identifier} is ready!")

async def on_node():
    node: wavelink.Node = wavelink.Node(uri="http://localhost:8000", password="password")
    await wavelink.NodePool.connect(client=bot, nodes=[node])

player: wavelink.Player = wavelink.Player
volume = 20


### NUNO ###


@bot.event
async def on_wavelink_track_end(self, interaction: nextcord.Interaction):
    global player
    print("da pizdec")
    try:
        await player.play(player.queue.get(), replace=False, populate=True)
    except:
        print("Пизда")



### COMMANDS ###


## test
@bot.slash_command(description="Тестовая команда", guild_ids=[])
async def test(interaction: nextcord.Interaction):
    await interaction.send("Я жива!")


## join
@bot.slash_command(guild_ids=[])
async def join(interaction: nextcord.Interaction):
    global player
    await interaction.response.send_message(f"Уже иду 0w0")
    try:
        player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    except:
        await player.move_to(interaction.user.voice.channel)

## leave
@bot.slash_command(guild_ids=[])
async def leave(interaction: nextcord.Interaction):
    global player
    await interaction.response.send_message(f"Зовите меня, когда захотите послушать музычку ^w^")
    await player.disconnect()

## pause
#@bot.slash_command(guild_ids=[])
#async def pause(interaction: nextcord.Interaction):
#    vc: wavelink.Player = interaction.guild.voice_client
#    try:
#        await vc.pause()
#        await interaction.response.send_message("=w= zᶻ")
#    except:
#        print("oi")

## resume
#@bot.slash_command(guild_ids=[])
#async def resume(interaction: nextcord.Interaction):
#    vc: wavelink.Player = interaction.guild.voice_client
#    try:
#        await vc.resume()
#        await interaction.response.send_message("0w0 !")
#    except:
#        print("io")

## stop
#@bot.slash_command(guild_ids=[])
#async def stop(interaction: nextcord.Interaction):
#    vc: wavelink.Player = interaction.guild.voice_client
#    vc.stop()
#    vc.cleanup()



## play
@bot.slash_command(guild_ids=[])
async def play(interaction: nextcord.Interaction):
    pass

@play.subcommand(description="Искать песиничку по названию")
async def search(interaction : nextcord.Interaction, query: str):
    global player, volume
    #destination = interaction.user.voice.channel

    #if not player.is_connected():
    #    await interaction.response.send_message("Позови меня с собой...")
    #    return

    await player.set_volume(volume)
    tracks = await wavelink.YouTubeTrack.search(query)

    if not tracks:
        await interaction.response.send_message(f"{query}: Не могу найти такую песиничку т.т")
        return
    
    await interaction.response.send_message(f"Песиничка в очереди ^w^\n{tracks[0].title}")
    player.auto_queue.put(tracks[0])

    if not player.is_playing():
        await player.play(player.auto_queue.get(), replace=False)


## link
@play.subcommand(description="Играть песиничку с ютабчика по URL")
async def link(interaction : nextcord.Interaction, link: str):
    
    #destination = interaction.user.voice.channel
    

    #tracks = await wavelink.YouTubeTrack.search("Ocean Drive - Duke Dumont")
    pass



## queue
@bot.slash_command(description="Показывает очередь песиничек", guild_ids=[])
async def queue(interaction: nextcord.Interaction):
    global player
    if not player.auto_queue.is_empty:
        queue = player.auto_queue.copy()
        songs = []
        song_count = 0
        for song in queue:
            song_count += 1
            songs.append(song)
        await interaction.response.send_message(queue)
    else:
        await interaction.response.send_message("Очередь пуста!")


bot.run("token")