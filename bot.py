# Créé par Lulu-76450 et l'IA (GPT ou Gemini)
# Sous license CC-BY, voir le fichier LICENSE
# (c) Lulu-76450 2025
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import requests
from discord import ui
from discord import app_commands
from discord.app_commands import MissingPermissions
from discord.ui import View, Button
from server import keep_alive
import youtube_dl  # Nécessaire pour gérer les streams audio
from detection_declenchement import setup_bot


# Charger le token depuis le fichier .env
load_dotenv()

# Dictionnaire pour suivre les salons privés temporaires des utilisateurs
user_private_channels = {}
locked_channels = {}
secure_mode = False

# Configuration des IDs (à remplacer par vos vrais IDs)
CHANNEL_ANNONCES_ID = os.getenv('CHANNEL_ANNONCES_ID')
ROLE_NOTIFS_ID = os.getenv('ROLE_NOTIFS_ID')
# Récupérer le token du bot
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


# Configuration des intents
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

# --- Événement de démarrage du bot ---
@bot.event
async def on_ready():
    """
    Cet événement est déclenché une fois que le bot est connecté à Discord.
    Toute la configuration du démarrage se fait ici.
    """
    print(f'Connecté en tant que {bot.user}')
    print(f'N E X U S B O T - Le Nexus Bot est en marche !')
    print(f'N E X U S B O T - Crédits : développé par Lulu-76450, open-source sur GitHub')

    # Liste de toutes les extensions à charger
    extensions = [
        'debile',
        'quiz',
        'mistralai',
        'antiraid',
        'fuzzy_listener',
        'ia' # L'extension que nous voulons
    ]

    # Charge toutes les extensions de manière asynchrone
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f'N E X U S B O T - L\'extension "{extension}" a été chargée avec succès.')
        except Exception as e:
            print(f"N E X U S B O T - Erreur lors du chargement de l'extension '{extension}': {e}")
    
    # Synchronise toutes les commandes slash APRES que les extensions ont été chargées.
    # Ceci est crucial pour que la commande /ia soit trouvée.
    try:
        await bot.tree.sync()
        print(f"N E X U S B O T - Commandes slash synchronisées. {len(bot.tree.get_commands())} commande(s) trouvée(s).")
    except Exception as e:
        print(f"N E X U S B O T - Erreur lors de la synchronisation des commandes : {e}")

@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        embed = discord.Embed(
            title="Je suis Nexus Bot",
            description="Un bot open source par Lulu-76450",
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# Gestionnaire d'erreurs global pour les commandes de préfixe.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass # Ignore les erreurs de commandes non trouvées.
    else:
        print(f"N E X U S B O T - Une erreur est survenue dans une commande : {error}")

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
    "{member.display.name}, t'es une personne vraiment cool et positive ! 😎"
]

# Section de démarrage du bot
if __name__ == "__main__":
    if DISCORD_BOT_TOKEN:
        bot.run(DISCORD_BOT_TOKEN)
    else:
        print("N E X U S B O T - Erreur: Le token Discord n'est pas défini. Veuillez le configurer dans le fichier .env.")

# Commande Slash pour lancer un dé
@bot.tree.command(name='de', description='Lance un dé avec un nombre de faces de ton choix.')
async def de(interaction: discord.Interaction, faces: int = 6):
    roll_result = random.randint(1, faces)
    await interaction.response.send_message(f"Tu as lancé un dé à {faces} faces et tu as obtenu : {roll_result}")

# Lire les blagues depuis le blagues.txt
def lire_blagues():
    with open('blagues.txt', 'r') as f:
        blagues = f.readlines()
    return [blague.strip() for blague in blagues]

# Commande Slash pour changer le statut du bot
@bot.tree.command(name='statusbot', description='Change le statut du bot avec un message personnalisé.')
async def statusbot(interaction: discord.Interaction, statut: str):
    activity = discord.Game(name=statut)
    await bot.change_presence(activity=activity)
    await interaction.response.send_message(f"Le statut du bot a été changé en : {statut}")

# Commande Slash pour envoyer un compliment
@bot.tree.command(name='compliment', description='Envoie un compliment à un utilisateur !')
async def compliment(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    compliment_message = random.choice(COMPLIMENTS).format(member=member)
    await interaction.response.send_message(compliment_message)

# Commande Slash pour afficher la latence
@bot.tree.command(name="ping", description="Affiche la latence du bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # En ms
    await interaction.response.send_message(f"Pong ! Latence : `{latency}ms`")

# Code déjà initialisé pour la gestion des messages
@bot.event
async def on_message(message):
    if message.author.bot:
        return


# Définition de la classe ConfirmationView
class ConfirmationView(View):
    def __init__(self, user, content):
        super().__init__()
        self.user = user
        self.content = content
        self.confirmed = False

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.user.id:
            self.confirmed = True
            self.stop()
        else:
            await interaction.response.send_message("Vous ne pouvez pas interagir avec cette confirmation.", ephemeral=True)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.user.id:
            self.confirmed = False
            self.stop()
        else:
            await interaction.response.send_message("Vous ne pouvez pas interagir avec cette confirmation.", ephemeral=True)

# Commande Slash pour envoyer une news
@bot.tree.command(name="envoyer_news", description="Envoyer une news dans le salon annonces")
@app_commands.checks.has_permissions(administrator=True)
async def envoyer_news(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)  # Réponse différée pour éviter les erreurs de délai
    await interaction.followup.send("Que souhaitez-vous inclure ?", ephemeral=True)

    def check(m):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    try:
        # Attente de la réponse de l'utilisateur
        msg = await bot.wait_for("message", check=check, timeout=600)

        # Création de la vue de confirmation
        view = ConfirmationView(interaction.user, msg.content)
        await interaction.followup.send("Cliquez pour confirmer ou annuler :", view=view, ephemeral=True)

        # Attente de l'interaction avec la vue
        await view.wait()

        if view.confirmed:
            # Récupération du salon et du rôle
            salon = bot.get_channel(int(os.getenv('CHANNEL_ANNONCES_ID')))
            role = interaction.guild.get_role(int(os.getenv('ROLE_NOTIFS_ID')))

            if not salon:
                await interaction.followup.send("Erreur : le salon des annonces est introuvable.", ephemeral=True)
                return
            if not role:
                await interaction.followup.send("Erreur : le rôle pour les notifications est introuvable.", ephemeral=True)
                return

            # Création et envoi de l'embed
            embed = discord.Embed(
                title="NEWS",
                description=msg.content,
                color=discord.Color.from_rgb(88, 101, 242)
            )
            await salon.send(f"{role.mention}", embed=embed)
            await interaction.followup.send("News envoyée !", ephemeral=True)
        else:
            await interaction.followup.send("Envoi annulé.", ephemeral=True)

    except asyncio.TimeoutError:
        await interaction.followup.send("Temps écoulé, veuillez recommencer la commande.", ephemeral=True)

# Gestion des erreurs de permissions
@envoyer_news.error
async def envoyer_news_error(interaction: discord.Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message(
            "Vous devez être administrateur pour utiliser cette commande !", ephemeral=True
        )
# embed des infos du bot
@bot.tree.command(name="infobot", description="Affiche les informations du bot.")
async def infobot(interaction):
    # Date de création fixée au 16 avril 2025
    creation_date = "16 avril 2025"

    embed = discord.Embed(
        title="Nexus Bot",
        description="Bot Discord Open-Source\n\nCode source : [GitHub Repository](https://github.com/Creatif-France-Games/nexus-bot/)",
        color=discord.Color.blue() 
    )
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")  # Ajoute l'avatar du bot (si dispo)
    embed.add_field(name="Date de création", value=creation_date, inline=False)
    embed.set_footer(text="Merci d'utiliser Nexus Bot !")

    # Envoi de l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="Affiche l'avatar d'un membre")
async def avatar(interaction: discord.Interaction, membre: discord.Member = None):
    membre = membre or interaction.user
    avatar_url = membre.avatar.url if membre.avatar else membre.default_avatar.url
    await interaction.response.send_message(f"Avatar de {membre.display_name} : {avatar_url}")

# Lancer un minuteur
@bot.tree.command(name="minuteur", description="Lance un minuteur avec un nom personnalisé")
async def minuteur(interaction: discord.Interaction, duree: int, nom: str):
    await interaction.response.send_message(
        f"⏳ Minuteur **{nom}** lancé pour {duree} minute(s), {interaction.user.mention} !"
    )

    async def timer_task():
        try:
            await asyncio.sleep(duree * 60)
            await interaction.followup.send(f"⏰ Le minuteur **{nom}** est terminé, {interaction.user.mention} !")
        except asyncio.CancelledError:
            await interaction.followup.send(f"❌ Le minuteur **{nom}** a été annulé, {interaction.user.mention}.")

    task = asyncio.create_task(timer_task())
    active_minuteurs[interaction.user.id] = task


@bot.tree.command(name="annule_minuteur", description="Annule ton minuteur en cours")
async def annule_minuteur(interaction: discord.Interaction):
    task = active_minuteurs.get(interaction.user.id)
    if task and not task.done():
        task.cancel()
        await interaction.response.send_message(f"🛑 Ton minuteur a été annulé, {interaction.user.mention}.")
        del active_minuteurs[interaction.user.id]
    else:
        await interaction.response.send_message("⚠️ Tu n’as pas de minuteur actif à annuler.")

# Commande /dire
@bot.tree.command(name="dire", description="Envoie un message personnalisé dans le canal.")
@app_commands.checks.has_permissions(administrator=True)
async def dire(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message) 

# Gestion des erreurs pour la commande /dire si l'utilisateur n'est pas admin
@dire.error
async def dire_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Désolé, vous devez être un administrateur pour utiliser cette commande.")

# Fonction asynchrone pour obtenir une blague en JSON
async def get_joke():
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous?lang=fr&blacklistFlags=nsfw,religious,racist,sexist,explicit"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("type") == "single":
                    return data.get("joke")
                elif data.get("type") == "twopart":
                    return f"{data.get('setup')}\n{data.get('delivery')}"
            return "Impossible de récupérer une blague."

# Slash command qui fonctionne vraiment
@bot.tree.command(name="blague", description="Obtiens une blague !")
async def blague(interaction: discord.Interaction):
    await interaction.response.defer()  # évite le timeout Discord
    joke = await get_joke()
    embed = discord.Embed(
        title="Blague du jour",
        description=joke,
        color=discord.Color.orange()
    )
    embed.set_footer(text="Via JokeAPI | /blague")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="embed", description="Envoie un message sous forme d'embed avec une couleur bleue.")
@app_commands.checks.has_permissions(administrator=True)
async def embed(interaction: discord.Interaction, titre: str, description: str):
    # Crée un embed avec les informations fournies
    embed = discord.Embed(
        title=titre,
        description=description,
        color=discord.Color.blue()  # Couleur bleue
    )
    
    # Envoie l'embed dans le canal
    await interaction.response.send_message(embed=embed)

@embed.error
async def embed_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "Désolé, vous devez être un administrateur pour utiliser cette commande.",
            ephemeral=True  # Message visible uniquement par l'utilisateur
        )

@bot.tree.command(name="bannir", description="Bannir un utilisateur avec une raison.")
@app_commands.checks.has_permissions(administrator=True)
async def bannir(interaction: discord.Interaction, membre: discord.Member, raison: str):
    try:
        # Envoi du message privé à l'utilisateur banni
        await membre.send(f"Vous avez été banni du serveur **{interaction.guild.name}** pour la raison suivante : {raison}")
    except discord.Forbidden:
        # Si l'utilisateur a les MP désactivés ou bloqués
        await interaction.response.send_message(
            f"Impossible d'envoyer un message privé à {membre.display_name}, mais il sera quand même banni.",
            ephemeral=True
        )
    except Exception as e:
        # Gestion des autres erreurs
        await interaction.response.send_message(
            f"Une erreur inattendue s'est produite : {e}",
            ephemeral=True
        )
        return

    # Bannir l'utilisateur
    await interaction.guild.ban(membre, reason=raison)
    
    # Répondre dans le canal
    await interaction.response.send_message(f"{membre.display_name} a été banni pour la raison suivante : {raison}")

@bot.tree.command(name="kick", description="Expulse un utilisateur du serveur avec une raison.")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, membre: discord.Member, raison: str):
    try:
        # Envoi du message privé à l'utilisateur expulsé
        await membre.send(f"Vous avez été expulsé du serveur **{interaction.guild.name}** pour la raison suivante : {raison}")
    except discord.Forbidden:
        # Si l'utilisateur a les MP désactivés ou bloqués
        await interaction.response.send_message(
            f"Impossible d'envoyer un message privé à {membre.display_name}, mais il sera quand même expulsé.",
            ephemeral=True
        )
    except Exception as e:
        # Gestion des autres erreurs
        await interaction.response.send_message(
            f"Une erreur inattendue s'est produite : {e}",
            ephemeral=True
        )
        return

    # Expulser l'utilisateur
    await interaction.guild.kick(membre, reason=raison)
    
    # Répondre dans le canal
    await interaction.response.send_message(f"{membre.display_name} a été expulsé pour la raison suivante : {raison}")
    
@bot.tree.command(name="infoserveur", description="Affiche des informations détaillées sur le serveur.")
async def infoserveur(interaction: discord.Interaction):
    # Récupérer les informations sur le serveur
    guild = interaction.guild
    nom_serveur = guild.name
    proprietaire = guild.owner
    date_creation = guild.created_at.strftime("%d %B %Y à %H:%M:%S")
    nombre_membres = len(guild.members)
    nombre_bots = len([membre for membre in guild.members if membre.bot])
    nombre_humains = nombre_membres - nombre_bots
    roles = [role.mention for role in guild.roles if role.name != "@everyone"]  # Exclure @everyone
    emojis = [str(emoji) for emoji in guild.emojis]
    niveau_boost = guild.premium_tier
    boosts = guild.premium_subscription_count

    # Créer un embed pour afficher les informations
    embed = discord.Embed(
        title=f"Informations sur le serveur : {nom_serveur}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Propriétaire", value=proprietaire.mention, inline=False)
    embed.add_field(name="Date de création", value=date_creation, inline=False)
    embed.add_field(name="Membres", value=f"Total : {nombre_membres}\nHumains : {nombre_humains}\nBots : {nombre_bots}", inline=False)
    embed.add_field(name="Niveau de boost", value=f"Niveau {niveau_boost} ({boosts} boosts)", inline=False)
    embed.add_field(name="Rôles", value=", ".join(roles) if roles else "Aucun rôle", inline=False)
    embed.add_field(name="Emojis", value=", ".join(emojis) if emojis else "Aucun emoji", inline=False)

    # Envoyer l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="infomembre", description="Affiche des informations sur un membre du serveur.")
async def infomembre(interaction: discord.Interaction, membre: discord.Member):
    # Récupérer les informations du membre
    nom = membre.name
    pseudo = membre.nick if membre.nick else "Aucun"
    date_creation_discord = membre.created_at.strftime("%d %B %Y à %H:%M:%S")
    date_rejoignage_serveur = membre.joined_at.strftime("%d %B %Y à %H:%M:%S") if membre.joined_at else "Inconnu"
    roles = [role.mention for role in membre.roles if role.name != "@everyone"]

    # Créer un embed pour afficher les informations
    embed = discord.Embed(
        title=f"Informations sur {nom}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Nom", value=nom, inline=False)
    embed.add_field(name="Pseudo (dans le serveur)", value=pseudo, inline=False)
    embed.add_field(name="Date de création du compte Discord", value=date_creation_discord, inline=False)
    embed.add_field(name="Date de rejoignage du serveur", value=date_rejoignage_serveur, inline=False)
    embed.add_field(name="Rôles", value=", ".join(roles) if roles else "Aucun rôle", inline=False)

    # Envoyer l'embed
    await interaction.response.send_message(embed=embed)

import datetime

@bot.tree.command(name="mute", description="Rend un membre muet pour une durée spécifiée.")
@app_commands.checks.has_permissions(administrator=True)
async def mute(interaction: discord.Interaction, membre: discord.Member, duree: int):
    # Vérifie si le rôle "Muted" existe
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not mute_role:
        await interaction.response.send_message(
            "Le rôle 'Muted' n'existe pas. Veuillez le créer et configurer ses permissions.",
            ephemeral=True
        )
        return

    # Ajoute le rôle "Muted" au membre
    await membre.add_roles(mute_role, reason=f"Muted par {interaction.user} pour {duree} minutes")
    await interaction.response.send_message(
        f"{membre.mention} a été rendu muet pour {duree} minutes.",
        ephemeral=False
    )

    # Planifie la suppression du rôle après la durée spécifiée
    await asyncio.sleep(duree * 60)  # Convertit la durée de minutes en secondes
    if mute_role in membre.roles:
        await membre.remove_roles(mute_role, reason="Durée de mute expirée")
        try:
            await membre.send(f"Vous n'êtes plus muet sur le serveur **{interaction.guild.name}**.")
        except discord.Forbidden:
            pass  # Si l'utilisateur a désactivé les MP

@bot.tree.command(name="qr", description="Génère un code QR à partir d'un texte ou d'une URL.")
async def qr(interaction: discord.Interaction, texte: str):
    # URL de l'API pour générer le code QR
    qr_url = f"https://quickchart.io/qr?text={texte}"
    
    # Créer un embed avec le code QR
    embed = discord.Embed(
        title="Code QR généré",
        description=f"Voici votre code QR pour : `{texte}`",
        color=discord.Color.blue()
    )
    embed.set_image(url=qr_url)  # Ajoute l'image du QR code
    embed.set_footer(text="Généré avec QuickChart.io")
    
    # Envoie l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bombe", description="Effectue un compte à rebours avant une explosion.")
async def bombe(interaction: discord.Interaction):
    await interaction.response.defer()  # Évite le timeout Discord pour les longues tâches
    
    # Liste du compte à rebours
    countdown = ["5", "4", "3", "2", "1"]
    
    # Message initial
    message = await interaction.followup.send("Ça va exploser : 5")
    await asyncio.sleep(1)
    
    # Modifier le message pour chaque étape du compte à rebours
    for i in range(1, len(countdown)):
        await message.edit(content=f"Ça va exploser : {countdown[i]}")
        await asyncio.sleep(1)
    
    # Remplace le message par le GIF de l'explosion
    await message.edit(content="💥 BOUM 💥\nhttps://c.tenor.com/uBrOl8WjH-EAAAAd/tenor.gif")
    await asyncio.sleep(3)
    
    # Supprime le message
    await message.delete()

# Commande Slash pour récupérer la température
@bot.tree.command(name="temperature", description="Affiche la température d'une ville.")
@app_commands.describe(ville="La ville pour laquelle afficher la température.")
async def temperature(interaction: discord.Interaction, ville: str):
    # Construire l'URL de l'API
    url = f"https://wttr.in/{ville}?format=%t"

    try:
        # Envoyer la requête à l'API
        response = requests.get(url)
        if response.status_code == 200:
            temperature = response.text.strip()  # Récupérer la température (nettoyer les espaces)
            
            # Créer un embed bleu
            embed = discord.Embed(
                title=f"Température de {ville.capitalize()}",
                description=f"**{temperature}**",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Via l'API wttr.in")

            # Envoyer l'embed
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"❌ Impossible de récupérer la température pour **{ville}**. Vérifiez l'orthographe ou réessayez plus tard.",
                ephemeral=True
            )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue en récupérant la température : {str(e)}",
            ephemeral=True
        )

# Commande Slash pour Rickroll
@bot.tree.command(name="rickroll", description="Envoie un Rickroll en message privé à un membre.")
@app_commands.describe(membre="Le membre à Rickroller.")
async def rickroll(interaction: discord.Interaction, membre: discord.Member):
    try:
        # Message Rickroll
        message = f"La personne {interaction.user.display_name} souhaite te partager cette vidéo : <https://youtu.be/dQw4w9WgXcQ?si=Hpc6awRKbIBqN3ws>"
        
        # Envoyer un message privé au membre
        await membre.send(message)
        
        # Répondre dans le salon pour confirmer l'envoi
        await interaction.response.send_message(f"Rickroll envoyé à {membre.display_name} !", ephemeral=True)
    except discord.Forbidden:
        # Si l'utilisateur a désactivé les MP
        await interaction.response.send_message(
            f"Impossible d'envoyer un message privé à {membre.display_name}.",
            ephemeral=True
        )
    except Exception as e:
        # Gestion des autres erreurs
        await interaction.response.send_message(
            f"Une erreur inattendue s'est produite : {str(e)}",
            ephemeral=True
        )

# Commande Slash pour un exercice de respiration
@bot.tree.command(name="respiration_exercice", description="Lance un exercice de respiration guidée (1 minute).")
async def respiration_exercice(interaction: discord.Interaction):
    try:
        # Informer l'utilisateur que l'exercice va commencer
        await interaction.response.send_message("Préparez-vous... L'exercice de respiration va commencer dans 5 secondes !")
        await asyncio.sleep(5)  # Pause initiale de 5 secondes

        # Variables pour contrôler le temps de l'exercice
        total_duration = 60  # Durée totale de l'exercice en secondes
        cycle_duration = 19  # Durée d'un cycle complet (inspirez 5s + expirez 5s + attendez 4s)
        cycles = total_duration // cycle_duration  # Nombre total de cycles (60 / 19)

        # Lancer l'exercice de respiration
        for cycle in range(cycles):
            for phase, phase_text, duration in [
                ("inspirez", "Inspirez...", 5),
                ("expirez", "Expirez...", 5),
                ("attendez", "Attendez...", 4),
            ]:
                # Créer un compte à rebours pour chaque étape
                for countdown in range(duration, 0, -1):
                    await interaction.channel.send(f"**{countdown}** {phase_text}")
                    await asyncio.sleep(1)

        # Fin de l'exercice
        await interaction.channel.send("🎉 Exercice de respiration terminé ! Bravo ! 🎉")

    except Exception as e:
        # Gestion des erreurs
        await interaction.followup.send(f"❌ Une erreur est survenue pendant l'exercice : {str(e)}", ephemeral=True)

# Commande Slash pour jouer une radio
@bot.tree.command(name="radio", description="Joue une station de radio dans votre salon vocal.")
@app_commands.describe(radio="Le nom de la station de radio.")
async def radio(interaction: discord.Interaction, radio: str):
    # Vérifiez si l'utilisateur est dans un salon vocal
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ Vous devez être dans un salon vocal pour utiliser cette commande.", ephemeral=True)
        return

    # Rejoindre le salon vocal
    voice_channel = interaction.user.voice.channel
    voice_client = await voice_channel.connect()

    # Récupérer la liste des radios via l'API Radio-Browser
    url = "https://de1.api.radio-browser.info/json/stations/bycountry/France"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await interaction.response.send_message("❌ Impossible de récupérer les stations de radio. Réessayez plus tard.", ephemeral=True)
                return

            radios = await response.json()
            # Trouver la radio correspondante
            station = next((r for r in radios if radio.lower() in r["name"].lower()), None)
            if not station:
                await interaction.response.send_message(f"❌ La station de radio `{radio}` est introuvable.", ephemeral=True)
                await voice_client.disconnect()
                return

            stream_url = station["url"]
            await interaction.response.send_message(f"🎵 Lecture de `{station['name']}` dans {voice_channel.name}...")

            # Jouer le stream audio
            try:
                ydl_opts = {"format": "bestaudio/best", "quiet": True}
                ffmpeg_opts = {
                    "options": "-vn",
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(stream_url, download=False)
                    url2play = info["url"]

                voice_client.play(discord.FFmpegPCMAudio(url2play, **ffmpeg_opts))
            except Exception as e:
                await interaction.response.send_message(f"❌ Une erreur s'est produite en jouant la radio : {e}", ephemeral=True)
                await voice_client.disconnect()
                return

            # Déconnecter après la fin
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()

# embed des serveurs
@bot.tree.command(name="serveurs", description="Affiche les serveurs MultiCraft de CF Games.")
async def infobot(interaction):

    embed = discord.Embed(
        title="Serveurs",
        description="Veloria (Code d'invitation : 3D5G9O1G)\n\Créatif France (Code d'invitation : 432IBSK4).",
        color=discord.Color.blue() 
    )
    embed.set_footer(text="Serveurs de CF Games")

    # Envoi de l'embed
    await interaction.response.send_message(embed=embed)

        # embed des serveurs
@bot.tree.command(name="pubcoolos", description="Affiche les serveurs MultiCraft de CF Games.")
async def infobot(interaction):

    embed = discord.Embed(
        title="Cool OS",
        description="Cool OS est un système d'exploitation par navigateur (https://www.cool-os.fr.nf), rejoignez le Discord directement depuis le site !",
        color=discord.Color.blue() 
    )
    embed.set_footer(text="Cool OS")

    # Envoi de l'embed
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Supprime des messages.")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("T'as pas les permitions... 😬", ephemeral=True)
        return

    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"{amount} messages supprimés", ephemeral=True)

@bot.tree.command(name="8ball", description="Pose ta question, la boule magique répond.")
async def ball(interaction: discord.Interaction, question: str):
    import random
    réponses = ["Oui", "Non", "Peut-être", "Demande à ton chat", "Jamais", "Carrément"]
    await interaction.response.send_message(f"🎱 {random.choice(réponses)}")

@bot.tree.command(name="devine", description="Devine un nombre entre 1 et 10.")
async def devine(interaction: discord.Interaction, nombre: int):
    import random
    secret = random.randint(1, 10)
    if nombre == secret:
        await interaction.response.send_message("🔮 Bien joué, t'as deviné !")
    else:
        await interaction.response.send_message(f"Raté ! C'était {secret}")

@bot.tree.command(name="pileface", description="Pile ou face !")
async def pileface(interaction: discord.Interaction):
    import random
    résultat = random.choice(["Pile", "Face"])
    await interaction.response.send_message(f"🪙 Résultat : {résultat}")

@bot.tree.command(name="chifoumi", description="Pierre, Feuille ou Ciseaux contre le bot.")
async def chifoumi(interaction: discord.Interaction, choix: str):
    import random
    choix = choix.lower()
    options = ["pierre", "feuille", "ciseaux"]
    bot_choix = random.choice(options)
    
    if choix not in options:
        await interaction.response.send_message("Choix invalide mec. Tape pierre, feuille ou ciseaux.")
        return

    résultat = {
        ("pierre", "ciseaux"): "Gagné !",
        ("feuille", "pierre"): "Gagné !",
        ("ciseaux", "feuille"): "Gagné !",
    }

    if choix == bot_choix:
        msg = f"Égalité ! On a tous les deux choisi {choix}."
    elif (choix, bot_choix) in résultat:
        msg = f"Tu gagnes ! ({choix} bat {bot_choix})"
    else:
        msg = f"Perdu ! ({bot_choix} bat {choix})"

    await interaction.response.send_message(msg)

@bot.tree.command(name="spam", description="Spammer 50 fois 'TEST SPAM' pour tester les protections anti-spam (réservé aux admins).")
@app_commands.checks.has_permissions(administrator=True)
async def spam(interaction: discord.Interaction):
    await interaction.response.send_message("Début du test de spam...", ephemeral=True)

    # Envoyer 50 messages "TEST SPAM"
    for _ in range(50):
        await interaction.channel.send("TEST SPAM")

@spam.error
async def spam_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "❌ Vous devez être administrateur pour utiliser cette commande.",
            ephemeral=True
        )

@bot.tree.command(name="salon_prive_temporaire", description="Créer un salon textuel temporaire (effacé après 1 heure).")
async def salon_prive_temporaire(interaction: discord.Interaction, nom_salon: str):
    user_id = interaction.user.id

    # Vérifier si l'utilisateur a déjà 2 salons privés
    if user_id in user_private_channels and len(user_private_channels[user_id]) >= 2:
        await interaction.response.send_message(
            "❌ Vous avez atteint la limite de 2 salons privés. Veuillez supprimer un salon existant avant d'en créer un nouveau.",
            ephemeral=True
        )
        return

    # Créer un salon privé dans la catégorie "Salons Privés" (à configurer selon votre serveur)
    category = discord.utils.get(interaction.guild.categories, name="Salons Privés")
    if not category:
        await interaction.response.send_message(
            "❌ La catégorie 'Salons Privés' n'existe pas. Veuillez la créer ou demander à un administrateur de l'ajouter.",
            ephemeral=True
        )
        return

    # Créer le salon
    channel = await interaction.guild.create_text_channel(
        name=nom_salon,
        category=category,
        overwrites={
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
    )

    # Ajouter le salon au dictionnaire
    if user_id not in user_private_channels:
        user_private_channels[user_id] = []
    user_private_channels[user_id].append(channel.id)

    # Planifier la suppression du salon après 1 heure
    await interaction.response.send_message(
        f"✅ Salon privé temporaire **{nom_salon}** créé avec succès. Il sera supprimé automatiquement après 1 heure.",
        ephemeral=True
    )
    await asyncio.sleep(3600)  # 1 heure en secondes
    await channel.delete()
    user_private_channels[user_id].remove(channel.id)

    # Nettoyer le dictionnaire si aucun salon n'existe
    if not user_private_channels[user_id]:
        del user_private_channels[user_id]

@bot.tree.command(name="ajouter_membre_salon", description="Ajouter un membre à votre salon privé temporaire.")
async def ajouter_membre_salon(interaction: discord.Interaction, salon_id: int, membre: discord.Member):
    user_id = interaction.user.id

    # Vérifier si le salon appartient à l'utilisateur
    if user_id not in user_private_channels or salon_id not in user_private_channels[user_id]:
        await interaction.response.send_message(
            "❌ Ce salon ne vous appartient pas ou n'existe pas.",
            ephemeral=True
        )
        return

    # Récupérer le salon
    channel = interaction.guild.get_channel(salon_id)
    if not channel:
        await interaction.response.send_message(
            "❌ Le salon spécifié est introuvable.",
            ephemeral=True
        )
        return

    # Ajouter les permissions au membre
    await channel.set_permissions(membre, read_messages=True, send_messages=True)
    await interaction.response.send_message(
        f"✅ {membre.mention} a été ajouté au salon privé temporaire **{channel.name}**.",
        ephemeral=True
    )

@tree.command(name="securisation", description="Active la sécurisation temporaire du serveur")
@app_commands.describe(duree="Durée en minutes")
async def securisation(interaction: discord.Interaction, duree: int):
    global secure_mode
    if secure_mode:
        await interaction.response.send_message("Sécurisation déjà en cours", ephemeral=True)
        return

    secure_mode = True
    locked_channels.clear()

    for channel in interaction.guild.text_channels:
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        if overwrite.send_messages is not False:
            locked_channels[channel.id] = overwrite.send_messages
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await channel.send("# Sécurisation\nIl est possible que le serveur subisse une cyberattaque. Par mesure de sécurité, toutes les actions sont limitées temporairement.")

    await interaction.response.send_message(f"Serveur sécurisé pour {duree} minutes", ephemeral=True)

    await asyncio.sleep(duree * 60)
    await securisation_fin_auto(interaction.guild)

@tree.command(name="securisation_fin", description="Désactive la sécurisation")
async def securisation_fin(interaction: discord.Interaction):
    await securisation_fin_auto(interaction.guild)
    await interaction.response.send_message("Sécurisation désactivée", ephemeral=True)

async def securisation_fin_auto(guild: discord.Guild):
    global secure_mode
    if not secure_mode:
        return

    for channel in guild.text_channels:
        if channel.id in locked_channels:
            overwrite = channel.overwrites_for(guild.default_role)
            overwrite.send_messages = locked_channels[channel.id]
            await channel.set_permissions(guild.default_role, overwrite=overwrite)
            await channel.send("✅ Sécurisation terminée. Le serveur est de nouveau accessible.")

    secure_mode = False
    locked_channels.clear()

@tree.command(name="maintenance", description="Active le mode maintenance")
@app_commands.describe(duree="Durée en minutes", raison="Raison de la maintenance")
async def maintenance(interaction: discord.Interaction, duree: int, raison: str):
    for channel in interaction.guild.text_channels:
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await channel.send(f"# Maintenance\n🛠️ Le serveur est en maintenance pour {duree} minutes.\n**Raison :** {raison}")

    await interaction.response.send_message(f"Maintenance activée pour {duree} minutes", ephemeral=True)
    await asyncio.sleep(duree * 60)

    for channel in interaction.guild.text_channels:
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await channel.send("✅ Fin de la maintenance. Merci de votre patience !")

# Supprimer la commande si elle existe déjà
if bot.tree.get_command('nouvel_article'):
    bot.tree.remove_command('nouvel_article')

@bot.tree.command(name="nouvel_article", description="Annonce un nouvel article sur le site (réservé aux admins).")
@app_commands.describe(titre="Un titre facultatif pour l'annonce.")
@app_commands.checks.has_permissions(administrator=True)
async def nouvel_article(interaction: discord.Interaction, titre: str = None):
    # Construire le message avec ou sans titre
    if titre:
        message = f"{titre}\nUn nouvel article est disponible sur [http://www.tech-tutos.netlify.app](http://www.tech-tutos.netlify.app)"
    else:
        message = "Un nouvel article est disponible sur [http://www.tech-tutos.netlify.app](http://www.tech-tutos.netlify.app)"
    
    # Envoyer le message
    await interaction.response.send_message(message, ephemeral=False)

# Gestion des erreurs pour les permissions
@nouvel_article.error
async def nouvel_article_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "❌ Vous devez être administrateur pour utiliser cette commande.",
            ephemeral=True
        )

# Code déjà initialisé pour garder le bot actif via Flask
keep_alive()

# Lancer le bot Discord
bot.run(os.getenv('DISCORD_TOKEN'))











