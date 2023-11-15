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
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(on_node())

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
   print(f"Node {node.identifier} is ready!")

async def on_node():
    node: wavelink.Node = wavelink.Node(uri="http://localhost:8000", password="password")
    await wavelink.NodePool.connect(client=bot, nodes=[node])

player: wavelink.Player = wavelink.Player



### COMMANDS ###


## test
@bot.slash_command(description="test", guild_ids=[])
async def test(interaction: nextcord.Interaction):
    await interaction.send("I am alive!")


## join
@bot.slash_command(guild_ids=[])
async def join(interaction: nextcord.Interaction):
    global player
    await interaction.response.send_message(f"im in 0w0")
    try:
        player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    except:
        await player.move_to(interaction.user.voice.channel)

## leave
@bot.slash_command(guild_ids=[])
async def leave(interaction: nextcord.Interaction):
    global player
    await interaction.response.send_message(f"Call me again soon ^w^")
    await player.disconnect()

## pause
#@bot.slash_command(guild_ids=[])
#async def pause(interaction: nextcord.Interaction):
#    vc: wavelink.Player = interaction.guild.voice_client
#    try:
#        await vc.pause()
#        await interaction.response.send_message("=w= zᶻ")
#    except:
#        pass

## resume
#@bot.slash_command(guild_ids=[])
#async def resume(interaction: nextcord.Interaction):
#    vc: wavelink.Player = interaction.guild.voice_client
#    try:
#        await vc.resume()
#        await interaction.response.send_message("0w0 !")
#    except:
#        pass

## stop
#@bot.slash_command(guild_ids=[])
#async def stop(interaction: nextcord.Interaction):
#    vc: wavelink.Player = interaction.guild.voice_client
#    vc.stop()
#    vc.cleanup()

## play
@bot.slash_command(guild_ids=[])
async def play():
    pass

@play.subcommand(description="===")
async def search(interaction : nextcord.Interaction, query: str):
    global player
    #destination = interaction.user.voice.channel

    if not player.is_connected():
        await interaction.response.send_message("let me join...")
        return
    
    #elif interaction.user.voice.channel.id != player.channel.id:
    #    await interaction.response.send_message("Чупачупсик, зайди в войсик <3")
    #    return

    await player.set_volume(30)
    player.auto_queue = True
    tracks = await wavelink.YouTubeTrack.search(query)
    await interaction.response.send_message(f"putting song to queue ^w^\n{tracks[0].title}")

    if not tracks:
        await interaction.response.send_message(f"{query}: not found т.т")
    else:
        await player.queue.put_wait(tracks[0])

    if not player.is_playing() and not player.is_paused():
        await player.play(player.queue.get(), populate=True)


bot.run("token")