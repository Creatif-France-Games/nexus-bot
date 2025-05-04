import discord
from discord.ext import commands
import youtube_dl
from discord import app_commands

# Commande Slash pour jouer de la musique
@bot.tree.command(name="play", description="Joue de la musique depuis YouTube.")
async def play(interaction: discord.Interaction, url: str):
    voice_channel = interaction.user.voice.channel
    if not voice_channel:
        await interaction.response.send_message("Tu dois être dans un canal vocal pour utiliser cette commande.", ephemeral=True)
        return

    # Se connecter au canal vocal
    voice_client = await voice_channel.connect()

    # Télécharger et lire la musique
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConverter',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))

    await interaction.response.send_message(f"Lecture de la musique depuis : {url}")

# Commande Slash pour arrêter la musique
@bot.tree.command(name="stop", description="Arrêter la musique.")
async def stop(interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("La musique a été arrêtée.")
    else:
        await interaction.response.send_message("Aucune musique en cours.")

# Commande Slash pour mettre en pause la musique
@bot.tree.command(name="pause", description="Met la musique en pause.")
async def pause(interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("La musique est en pause.")
    else:
        await interaction.response.send_message("Aucune musique en cours.")

# Commande Slash pour reprendre la musique
@bot.tree.command(name="resume", description="Reprendre la musique.")
async def resume(interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("La musique a été reprise.")
    else:
        await interaction.response.send_message("Aucune musique en pause.")
