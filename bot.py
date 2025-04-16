from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
from discord import ui
from discord import app_commands

# Initialisation de Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot actif !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Charger le token depuis le fichier .env
load_dotenv()

# Configuration des intents
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration des IDs (à remplacer par vos vrais IDs)
CHANNEL_ANNONCES_ID = os.getenv('CHANNEL_ANNONCES_ID')  # Utilisez une variable d'environnement
ROLE_NOTIFS_ID = os.getenv('ROLE_NOTIFS_ID')  # Utilisez une variable d'environnement

# Liste des blagues
BLAGUES = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent toujours dans le bateau.",
    "Pourquoi les poissons détestent-ils l'ordinateur ? Parce qu'ils ont peur du net.",
    "Quel est le comble pour un électricien ? De ne pas être au courant.",
    "Pourquoi les squelettes n’aiment-ils pas se battre ? Parce qu’ils n’ont pas de tripes.",
    "Quel est le comble pour un électricien ? De ne pas être au courant.",
    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent toujours dans le bateau."
]

# Liste des compliments
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

@bot.tree.command(name='de', description='Lance un dé avec un nombre de faces de ton choix.')
async def de(interaction: discord.Interaction, faces: int = 6):
    """Commande Slash pour lancer un dé"""
    roll_result = random.randint(1, faces)
    await interaction.response.send_message(f"Tu as lancé un dé à {faces} faces et tu as obtenu : {roll_result}")

@bot.tree.command(name='blague', description='Dis une blague drôle.')
async def blague(interaction: discord.Interaction):
    """Commande Slash pour donner une blague"""
    joke = random.choice(BLAGUES)
    await interaction.response.send_message(joke)

@bot.tree.command(name='statusbot', description='Change le statut du bot avec un message personnalisé.')
async def statusbot(interaction: discord.Interaction, statut: str):
    """Commande Slash pour changer le statut du bot"""
    activity = discord.Game(name=statut)
    await bot.change_presence(activity=activity)
    await interaction.response.send_message(f"Le statut du bot a été changé en : {statut}")

@bot.tree.command(name='compliment', description='Envoie un compliment à quelqu\'un !')
async def compliment(interaction: discord.Interaction, member: discord.Member = None):
    """Commande Slash pour donner un compliment à un utilisateur"""
    member = member or interaction.user  # Si personne n'est mentionné, donner un compliment à l'utilisateur qui a envoyé la commande.
    compliment_message = random.choice(COMPLIMENTS).format(member=member)
    await interaction.response.send_message(compliment_message)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    salutations = ["salut", "bonjour", "coucou", "hi", "hola", "hello", "yo", "re", "bonsoir"]
    depart = ["au revoir", "bye", "a+", "ciao", "see ya", "à bientôt", "adieu", "bonne nuit", "bn", "tchao"]
    faim = ["j'ai faim", "faim", "j’ai la dalle", "je crève de faim", "trop faim"]

    if any(word in content for word in salutations):
        await message.reply(f"Salut {message.author.mention} !")
    elif any(word in content for word in depart):
        await message.reply(f"Bye {message.author.mention} !")
    elif any(word in content for word in faim):
        await message.reply("Tiens une bonne assiette de pâtes carbonara :\nhttps://cdn.pixabay.com/photo/2011/04/29/11/20/spaghetti-7113_1280.jpg")
    
    await bot.process_commands(message)

@bot.tree.command(name="envoyer_news", description="Envoyer une news dans le salon annonces")
@app_commands.checks.has_permissions(administrator=True)
async def envoyer_news(interaction: discord.Interaction):
    await interaction.response.send_message("Que souhaitez-vous inclure ?", ephemeral=True)

    def check(m):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)

        view = ConfirmationView(interaction.user, msg.content)
        await interaction.followup.send("Clique pour confirmer ou annuler :", view=view, ephemeral=True)

        await view.wait()

        if view.confirmed:
            salon = bot.get_channel(CHANNEL_ANNONCES_ID)
            role = interaction.guild.get_role(ROLE_NOTIFS_ID)

            if salon and role:
                embed = discord.Embed(
                    title="NEWS",
                    description=msg.content,
                    color=discord.Color.from_rgb(88, 101, 242)
                )
                await salon.send(f"{role.mention}", embed=embed)
                await interaction.followup.send("News envoyée !", ephemeral=True)
            else:
                await interaction.followup.send("Erreur : salon ou rôle introuvable.", ephemeral=True)
        else:
            await interaction.followup.send("Envoi annulé.", ephemeral=True)

    except asyncio.TimeoutError:
        await interaction.followup.send("Temps écoulé, veuillez recommencer la commande.", ephemeral=True)

@bot.tree.command(name="ping", description="Affiche la latence du bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # En ms
    await interaction.response.send_message(f"Pong ! Latence : `{latency}ms`")

# Code déjà initialisé
keep_alive()

# Lancer le bot Discord
bot.run(os.getenv('DISCORD_TOKEN'))
