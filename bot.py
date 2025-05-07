import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
from discord import ui
from discord import app_commands
import wikipediaapi
from discord.app_commands import MissingPermissions
from discord.ui import View, Button
from server import keep_alive

# Charger le token depuis le fichier .env
load_dotenv()

# Configuration des intents
intents = discord.Intents.all()
intents.message_content = True

# Remplacer discord.Client par commands.Bot
bot = commands.Bot(command_prefix='!', intents=intents)  # Assure-toi que c'est un Bot et non un Client

# Charger les extensions dans un setup coroutine
async def on_ready():
    await bot.tree.sync()
    print(f'Connecté en tant que {bot.user} (commandes slash synchronisées)')

async def setup_extensions():
    await bot.load_extension("deepseek")
    await bot.load_extension("quiz")

# Compliments
COMPLIMENTS = [
    "{member.display_name}, tu es une personne incroyable ! 😄",
    "{member.display_name}, tu illumines la journée de tout le monde ! ✨",
    "{member.display_name}, tu as un sourire qui réchauffe le cœur ! 😊",
    "{member.display_name}, tu es un rayon de soleil dans ce monde ! 🌞",
    "{member.display_name}, tes idées sont toujours brillantes ! 💡",
    "{member.display_name}, tu as un grand cœur ! ❤️",
    "{member.display_name}, t'es vraiment une source d'inspiration ! 🌟",
    "{member.display_name}, ton énergie est contagieuse ! ⚡",
    "{member.display_name}, t'es une personne vraiment cool et positive ! 😎"
]

# Slash Commands
@bot.tree.command(name='wikipedia', description='Fais une recherche sur Wikipédia.')
async def wikipedia(interaction: discord.Interaction, recherche: str):
    wiki = wikipediaapi.Wikipedia('fr')
    page = wiki.page(recherche.strip())
    if not page.exists():
        await interaction.response.send_message(
            f"Aucune page trouvée pour : **{recherche}**.", ephemeral=True)
        return
    extrait = page.summary[:1000] + ("..." if len(page.summary) > 1000 else "")
    await interaction.response.send_message(f"**{page.title}**\n{extrait}\n[Lire plus ici]({page.fullurl})")

@bot.tree.command(name='de', description='Lance un dé avec un nombre de faces.')
async def de(interaction: discord.Interaction, faces: int = 6):
    result = random.randint(1, faces)
    await interaction.response.send_message(f"Tu as obtenu : {result}")

@bot.tree.command(name='blague', description='Dis une blague.')
async def blague(interaction: discord.Interaction):
    with open('blagues.txt', 'r') as f:
        blagues = [l.strip() for l in f.readlines()]
    await interaction.response.send_message(random.choice(blagues))

@bot.tree.command(name='statusbot', description='Change le statut du bot.')
async def statusbot(interaction: discord.Interaction, statut: str):
    await bot.change_presence(activity=discord.Game(name=statut))
    await interaction.response.send_message(f"Statut changé en : {statut}")

@bot.tree.command(name='compliment', description='Envoie un compliment.')
async def compliment(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    await interaction.response.send_message(random.choice(COMPLIMENTS).format(member=member))

@bot.tree.command(name="ping", description="Affiche la latence du bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong ! Latence : `{latency}ms`")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# Lancer les extensions et le bot dans une fonction asynchrone
async def main():
    # Charge les extensions
    await setup_extensions()
    # Démarre le bot
    token = os.getenv('DISCORD_TOKEN')
    await bot.start(token)

# Lancer le bot
keep_alive()
asyncio.run(main())  # Remplace `bot.run(token)` par asyncio.run(main()) pour démarrer le bot
