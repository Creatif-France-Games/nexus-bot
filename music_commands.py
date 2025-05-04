import yt_dlp
from discord import FFmpegPCMAudio
import discord

async def join(ctx: discord.Interaction):
    channel = ctx.user.voice.channel
    if channel:
        await channel.connect()
        await ctx.response.send_message(f"Je me connecte à {channel} !")
    else:
        await ctx.response.send_message("Tu dois être dans un canal vocal pour que je puisse te rejoindre.")

async def play(ctx: discord.Interaction, url: str):
    channel = ctx.user.voice.channel
    if not channel:
        await ctx.response.send_message("Tu dois être dans un canal vocal pour jouer de la musique.")
        return

    # Récupérer l'URL de la vidéo YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client = await channel.connect()

        # Jouer l'audio dans le canal vocal
        voice_client.play(FFmpegPCMAudio(url2))

    await ctx.response.send_message(f"Je joue maintenant la musique depuis {url} !")

async def stop(ctx: discord.Interaction):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.response.send_message("Je me déconnecte du canal vocal.")
    else:
        await ctx.response.send_message("Je ne suis pas connecté à un canal vocal.")

async def pause(ctx: discord.Interaction):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.response.send_message("La musique a été mise en pause.")
    else:
        await ctx.response.send_message("Aucune musique en cours de lecture.")

async def resume(ctx: discord.Interaction):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.response.send_message("La musique reprend.")
    else:
        await ctx.response.send_message("Il n'y a pas de musique en pause.")
