# Copyright CC-BY Team CF Games 2025, codé avec l'aide de Gemini
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import requests
import re # Importation pour les expressions régulières

# Charger le token depuis le fichier .env
load_dotenv()

# Dictionnaire pour suivre les salons privés temporaires des utilisateurs
user_private_channels = {}
locked_channels = {}
secure_mode = False # Variable non utilisée dans ce refactor, mais conservée

# Configuration des intents
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
# Le bot est initialisé ici, mais ne sera démarré que par le script principal
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Suppression de la synchronisation des commandes slash, car nous n'en avons plus.
    print(f'Connecté en tant que {bot.user} (déclenchement par instruction vocale)')
    print(f'Prêt à recevoir des instructions textuelles.')


# Initialisation d'une variable pour stocker les minuteurs actifs
active_minuteurs = {}

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

# Fonction utilitaire pour trouver un membre par nom ou pseudo
async def find_member_by_name(guild, name):
    # Cherche par mention d'abord
    mention_match = re.search(r'<@!?(\d+)>', name)
    if mention_match:
        member_id = int(mention_match.group(1))
        member = guild.get_member(member_id)
        if member:
            return member

    # Si pas de mention, cherche par nom ou pseudo
    name_lower = name.lower()
    for member in guild.members:
        if member.name.lower() == name_lower or \
           (member.nick and member.nick.lower() == name_lower):
            return member
    return None

# --- Fonctions de logique des commandes (anciennement les commandes slash) ---

async def de_logic(message: discord.Message, faces: int = 6):
    """Logique pour lancer un dé."""
    roll_result = random.randint(1, faces)
    await message.reply(f"Tu as lancé un dé à {faces} faces et tu as obtenu : {roll_result}")

async def compliment_logic(message: discord.Message, member: discord.Member = None):
    """Logique pour envoyer un compliment."""
    member = member or message.author
    compliment_message = random.choice(COMPLIMENTS).format(member=member)
    await message.reply(compliment_message)

async def ping_logic(message: discord.Message):
    """Logique pour afficher la latence."""
    latency = round(bot.latency * 1000)  # En ms
    await message.reply(f"Pong ! Latence : `{latency}ms`")

async def get_joke():
    """Fonction asynchrone pour obtenir une blague en JSON."""
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

async def blague_logic(message: discord.Message):
    """Logique pour obtenir une blague."""
    joke = await get_joke()
    embed = discord.Embed(
        title="Blague du jour",
        description=joke,
        color=discord.Color.orange()
    )
    embed.set_footer(text="Via JokeAPI | Demande à Nexus de raconter une blague")
    await message.reply(embed=embed)

async def infobot_logic(message: discord.Message):
    """Logique pour afficher les informations du bot."""
    creation_date = "16 avril 2025"
    embed = discord.Embed(
        title="CF Games Bot",
        description="Bot Discord Open-Source\n\nCode source : [GitHub Repository](https://github.com/Creatif-France-Games/cf-games-bot/)",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")
    embed.add_field(name="Date de création", value=creation_date, inline=False)
    embed.set_footer(text="Merci d'utiliser CF Games Bot !")
    await message.reply(embed=embed)

async def avatar_logic(message: discord.Message, membre: discord.Member = None):
    """Logique pour afficher l'avatar d'un membre."""
    membre = membre or message.author
    avatar_url = membre.avatar.url if membre.avatar else membre.default_avatar.url
    await message.reply(f"Avatar de {membre.display_name} : {avatar_url}")

async def minuteur_logic(message: discord.Message, duree: int, nom: str):
    """Logique pour lancer un minuteur."""
    await message.reply(
        f"⏳ Minuteur **{nom}** lancé pour {duree} minute(s), {message.author.mention} !"
    )

    async def timer_task():
        try:
            await asyncio.sleep(duree * 60)
            await message.channel.send(f"⏰ Le minuteur **{nom}** est terminé, {message.author.mention} !")
        except asyncio.CancelledError:
            await message.channel.send(f"❌ Le minuteur **{nom}** a été annulé, {message.author.mention}.")

    task = asyncio.create_task(timer_task())
    active_minuteurs[message.author.id] = task

async def annule_minuteur_logic(message: discord.Message):
    """Logique pour annuler un minuteur."""
    task = active_minuteurs.get(message.author.id)
    if task and not task.done():
        task.cancel()
        await message.reply(f"🛑 Ton minuteur a été annulé, {message.author.mention}.")
        del active_minuteurs[message.author.id]
    else:
        await message.reply("⚠️ Tu n’as pas de minuteur actif à annuler.")

async def infoserveur_logic(message: discord.Message):
    """Logique pour afficher les informations du serveur."""
    guild = message.guild
    nom_serveur = guild.name
    proprietaire = guild.owner
    date_creation = guild.created_at.strftime("%d %B %Y à %H:%M:%S")
    nombre_membres = len(guild.members)
    nombre_bots = len([membre for membre in guild.members if membre.bot])
    nombre_humains = nombre_membres - nombre_bots
    roles = [role.mention for role in guild.roles if role.name != "@everyone"]
    emojis = [str(emoji) for emoji in guild.emojis]
    niveau_boost = guild.premium_tier
    boosts = guild.premium_subscription_count

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
    await message.reply(embed=embed)

async def infomembre_logic(message: discord.Message, membre: discord.Member):
    """Logique pour afficher des informations sur un membre."""
    nom = membre.name
    pseudo = membre.nick if membre.nick else "Aucun"
    date_creation_discord = membre.created_at.strftime("%d %B %Y à %H:%M:%S")
    date_rejoignage_serveur = membre.joined_at.strftime("%d %B %Y à %H:%M:%S") if membre.joined_at else "Inconnu"
    roles = [role.mention for role in membre.roles if role.name != "@everyone"]

    embed = discord.Embed(
        title=f"Informations sur {nom}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Nom", value=nom, inline=False)
    embed.add_field(name="Pseudo (dans le serveur)", value=pseudo, inline=False)
    embed.add_field(name="Date de création du compte Discord", value=date_creation_discord, inline=False)
    embed.add_field(name="Date de rejoignage du serveur", value=date_rejoignage_serveur, inline=False)
    embed.add_field(name="Rôles", value=", ".join(roles) if roles else "Aucun rôle", inline=False)
    await message.reply(embed=embed)

async def qr_logic(message: discord.Message, texte: str):
    """Logique pour générer un code QR."""
    qr_url = f"https://quickchart.io/qr?text={texte}"
    embed = discord.Embed(
        title="Code QR généré",
        description=f"Voici votre code QR pour : `{texte}`",
        color=discord.Color.blue()
    )
    embed.set_image(url=qr_url)
    embed.set_footer(text="Généré avec QuickChart.io")
    await message.reply(embed=embed)

async def bombe_logic(message: discord.Message):
    """Logique pour un compte à rebours de bombe."""
    await message.channel.send("Ça va exploser : 5")
    await asyncio.sleep(1)
    for i in range(4, 0, -1):
        await message.channel.send(f"Ça va exploser : {i}")
        await asyncio.sleep(1)
    await message.channel.send("💥 BOUM 💥\nhttps://c.tenor.com/uBrOl8WjH-EAAAAd/tenor.gif")
    await asyncio.sleep(3)
    # Note: On ne peut pas supprimer un message du bot facilement sans avoir le message object retourné par send.
    # Pour un message de compte à rebours, il faudrait editer le même message au lieu d'en envoyer plusieurs.
    # Pour simplifier et correspondre à la structure on_message, on envoie des messages séparés ici.

async def temperature_logic(message: discord.Message, ville: str):
    """Logique pour récupérer la température d'une ville."""
    url = f"https://wttr.in/{ville}?format=%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            temperature = response.text.strip()
            embed = discord.Embed(
                title=f"Température de {ville.capitalize()}",
                description=f"**{temperature}**",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Via l'API wttr.in")
            await message.reply(embed=embed)
        else:
            await message.reply(
                f"❌ Impossible de récupérer la température pour **{ville}**. Vérifiez l'orthographe ou réessayez plus tard."
            )
    except Exception as e:
        await message.reply(
            f"❌ Une erreur est survenue en récupérant la température : {str(e)}"
        )

async def respiration_exercice_logic(message: discord.Message):
    """Logique pour un exercice de respiration."""
    try:
        await message.reply("Préparez-vous... L'exercice de respiration va commencer dans 5 secondes !")
        await asyncio.sleep(5)

        total_duration = 60
        # Les durées sont ajustées pour que le compte à rebours s'affiche correctement
        # Inspirez 5s (5,4,3,2,1)
        # Expirez 5s (5,4,3,2,1)
        # Attendez 4s (4,3,2,1)
        cycle_duration = 5 + 5 + 4 # Total 14 secondes par cycle d'instructions

        # Calculer le nombre de cycles pour que la durée totale soit d'environ 60 secondes.
        # On va faire 4 cycles (4 * 14 = 56s) + une petite pause à la fin pour atteindre 60s
        cycles = 4 # Ex: (Inspire, Expire, Attend) x 4 = 56s

        for cycle in range(cycles):
            for phase, phase_text, duration in [
                ("inspirez", "Inspirez...", 5),
                ("expirez", "Expirez...", 5),
                ("attendez", "Attendez...", 4),
            ]:
                for countdown in range(duration, 0, -1):
                    await message.channel.send(f"**{countdown}** {phase_text}")
                    await asyncio.sleep(1)
        
        # S'assurer que la durée totale approche les 60 secondes si les cycles ne couvrent pas tout
        remaining_time = total_duration - (cycles * cycle_duration)
        if remaining_time > 0:
            await message.channel.send(f"Quelques secondes supplémentaires...")
            await asyncio.sleep(remaining_time)

        await message.channel.send("🎉 Exercice de respiration terminé ! Bravo ! 🎉")

    except Exception as e:
        await message.reply(f"❌ Une erreur est survenue pendant l'exercice : {str(e)}")

# YouTube-DL est déprécié, il est recommandé d'utiliser yt-dlp à la place.
# youtube_dl est conservé pour la compatibilité avec le code original fourni.
import youtube_dl 

async def radio_logic(message: discord.Message, radio_name: str):
    """Logique pour jouer une station de radio."""
    if not message.author.voice or not message.author.voice.channel:
        await message.reply("❌ Vous devez être dans un salon vocal pour que Nexus joue la radio.")
        return

    voice_channel = message.author.voice.channel
    voice_client = None
    try:
        voice_client = await voice_channel.connect()
    except discord.ClientException:
        await message.reply("Nexus est déjà connecté à un salon vocal.")
        return
    except Exception as e:
        await message.reply(f"Une erreur est survenue lors de la connexion au salon vocal : {e}")
        return

    url = "https://de1.api.radio-browser.info/json/stations/bycountry/France"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.reply("❌ Nexus n'a pas pu récupérer les stations de radio. Réessayez plus tard.")
                if voice_client: await voice_client.disconnect()
                return

            radios = await response.json()
            station = next((r for r in radios if radio_name.lower() in r["name"].lower()), None)
            if not station:
                await message.reply(f"❌ Nexus n'a pas trouvé la station de radio `{radio_name}`.")
                if voice_client: await voice_client.disconnect()
                return

            stream_url = station["url"]
            await message.reply(f"🎵 Nexus joue `{station['name']}` dans {voice_channel.name}...")

            try:
                # Utilisation d'un dict vide pour ffmpeg_options car le code original n'utilisait pas d'options avancées
                ydl_opts = {"format": "bestaudio/best", "quiet": True}
                ffmpeg_opts = {"options": "-vn"} # options ffmpeg pour exclure la vidéo
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(stream_url, download=False)
                    url2play = info["url"]

                voice_client.play(discord.FFmpegPCMAudio(url2play, **ffmpeg_opts), after=lambda e: print(f'Player error: {e}') if e else None)
            except Exception as e:
                await message.reply(f"❌ Une erreur s'est produite en jouant la radio : {e}")
                if voice_client: await voice_client.disconnect()
                return

            # Attendre que la musique se termine si elle est un fichier de durée limitée
            # Pour les radios en direct, cela bouclera indéfiniment à moins d'un arrêt manuel
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()


async def serveurs_logic(message: discord.Message):
    """Logique pour afficher les serveurs MultiCraft."""
    embed = discord.Embed(
        title="Serveurs",
        description="Veloria (Code d'invitation : X72KP62P)\n\Créatif France (Code d'invitation : 432IBSK4)",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Serveurs de CF Games")
    await message.reply(embed=embed)

async def eightball_logic(message: discord.Message, question: str):
    """Logique pour la 8ball magique."""
    réponses = ["Oui", "Non", "Peut-être", "Demande à ton chat", "Jamais", "Carrément"]
    await message.reply(f"🎱 {random.choice(réponses)}")

async def devine_logic(message: discord.Message, nombre: int):
    """Logique pour le jeu de devinette de nombre."""
    secret = random.randint(1, 10)
    if nombre == secret:
        await message.reply("🔮 Bien joué, t'as deviné !")
    else:
        await message.reply(f"Raté ! C'était {secret}")

async def pileface_logic(message: discord.Message):
    """Logique pour le jeu de pile ou face."""
    résultat = random.choice(["Pile", "Face"])
    await message.reply(f"🪙 Résultat : {résultat}")

async def chifoumi_logic(message: discord.Message, choix: str):
    """Logique pour le jeu de pierre, feuille, ciseaux."""
    choix = choix.lower()
    options = ["pierre", "feuille", "ciseaux"]

    if choix not in options:
        await message.reply("Choix invalide mec. Dis pierre, feuille ou ciseaux.")
        return

    bot_choix = random.choice(options)

    résultat_mapping = {
        ("pierre", "ciseaux"): "Gagné !",
        ("feuille", "pierre"): "Gagné !",
        ("ciseaux", "feuille"): "Gagné !",
    }

    if choix == bot_choix:
        msg = f"Égalité ! On a tous les deux choisi {choix}."
    elif (choix, bot_choix) in résultat_mapping:
        msg = f"Tu gagnes ! ({choix} bat {bot_choix})"
    else:
        msg = f"Perdu ! ({bot_choix} bat {choix})"

    await message.reply(msg)

async def salon_prive_temporaire_logic(message: discord.Message, nom_salon: str):
    """Logique pour créer un salon textuel temporaire."""
    user_id = message.author.id

    if user_id in user_private_channels and len(user_private_channels[user_id]) >= 2:
        await message.reply(
            "❌ Vous avez atteint la limite de 2 salons privés. Veuillez supprimer un salon existant avant d'en créer un nouveau."
        )
        return

    category = discord.utils.get(message.guild.categories, name="Salons Privés")
    if not category:
        await message.reply(
            "❌ La catégorie 'Salons Privés' n'existe pas. Veuillez la créer ou demander à un administrateur de l'ajouter."
        )
        return

    channel = await message.guild.create_text_channel(
        name=nom_salon,
        category=category,
        overwrites={
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
    )

    if user_id not in user_private_channels:
        user_private_channels[user_id] = []
    user_private_channels[user_id].append(channel.id)

    await message.reply(
        f"✅ Salon privé temporaire **{nom_salon}** créé avec succès. Il sera supprimé automatiquement après 1 heure."
    )
    await asyncio.sleep(3600)
    # Vérifier si le salon existe toujours avant de tenter de le supprimer
    if channel and channel.id in user_private_channels.get(user_id, []):
        await channel.delete()
        user_private_channels[user_id].remove(channel.id)
        if not user_private_channels[user_id]:
            del user_private_channels[user_id]

async def ajouter_membre_salon_logic(message: discord.Message, salon_id: int, membre: discord.Member):
    """Logique pour ajouter un membre à un salon privé temporaire."""
    user_id = message.author.id

    if user_id not in user_private_channels or salon_id not in user_private_channels[user_id]:
        await message.reply(
            "❌ Ce salon ne vous appartient pas ou n'existe pas."
        )
        return

    channel = message.guild.get_channel(salon_id)
    if not channel:
        await message.reply(
            "❌ Le salon spécifié est introuvable."
        )
        return

    await channel.set_permissions(membre, read_messages=True, send_messages=True)
    await message.reply(
        f"✅ {membre.mention} a été ajouté au salon privé temporaire **{channel.name}**."
    )

# --- Gestionnaire de messages principal ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # --- Déclencheurs de commandes refactorisées ---
    # La priorité est donnée aux commandes spécifiques avant les réponses génériques.

    # Dé: "Nexus lance un dé (à X faces)" ou "Nexus fais un dé"
    match = re.search(r"nexus lance un dé( à (\d+) faces)?|nexus fais un dé( à (\d+) faces)?", content)
    if match:
        faces_str = match.group(2) or match.group(4) # Capture le nombre de faces
        faces = int(faces_str) if faces_str else 6
        await de_logic(message, faces)
        return

    # Compliment: "Nexus complimente @utilisateur" ou "Nexus fais un compliment à @utilisateur"
    match = re.search(r"nexus (complimente|fais un compliment à) (.+)", content)
    if match:
        member_name = match.group(2).strip()
        member = await find_member_by_name(message.guild, member_name)
        if member:
            await compliment_logic(message, member)
        else:
            await message.reply("❌ Nexus n'a pas pu trouver ce membre. Assurez-vous de le mentionner ou d'écrire son nom correctement.")
        return

    # Ping: "Nexus ping" ou "Nexus quelle est ta latence"
    if "nexus ping" in content or "nexus quelle est ta latence" in content:
        await ping_logic(message)
        return

    # Blague: "Nexus raconte une blague" ou "Nexus dis-moi une blague"
    if "nexus raconte une blague" in content or "nexus dis-moi une blague" in content:
        await blague_logic(message)
        return

    # Info bot: "Nexus info bot" ou "Nexus donne-moi tes infos"
    if "nexus info bot" in content or "nexus donne-moi tes infos" in content:
        await infobot_logic(message)
        return

    # Avatar: "Nexus montre l'avatar de @utilisateur" ou "Nexus quel est l'avatar de @utilisateur"
    match = re.search(r"nexus (montre l'avatar de|quel est l'avatar de) (.+)", content)
    if match:
        member_name = match.group(2).strip()
        member = await find_member_by_name(message.guild, member_name)
        if member:
            await avatar_logic(message, member)
        else:
            await message.reply("❌ Nexus n'a pas pu trouver ce membre. Assurez-vous de le mentionner ou d'écrire son nom correctement.")
        return
    
    # Minuteur: "Nexus lance un minuteur de X minutes pour Y"
    match = re.search(r"nexus lance un minuteur de (\d+) minutes? pour (.+)", content)
    if match:
        duree = int(match.group(1))
        nom = match.group(2).strip()
        await minuteur_logic(message, duree, nom)
        return
    
    # Annuler minuteur: "Nexus annule mon minuteur"
    if "nexus annule mon minuteur" in content:
        await annule_minuteur_logic(message)
        return

    # Info serveur: "Nexus info serveur" ou "Nexus donne les infos du serveur"
    if "nexus info serveur" in content or "nexus donne les infos du serveur" in content:
        await infoserveur_logic(message)
        return

    # Info membre: "Nexus info membre @utilisateur" ou "Nexus donne les infos de @utilisateur"
    match = re.search(r"nexus (info membre|donne les infos de) (.+)", content)
    if match:
        member_name = match.group(2).strip()
        member = await find_member_by_name(message.guild, member_name)
        if member:
            await infomembre_logic(message, member)
        else:
            await message.reply("❌ Nexus n'a pas pu trouver ce membre. Assurez-vous de le mentionner ou d'écrire son nom correctement.")
        return

    # QR: "Nexus génère un QR code pour [texte]" ou "Nexus fais un QR code de [texte]"
    match = re.search(r"nexus (génère un qr code pour|fais un qr code de) (.+)", content)
    if match:
        texte = match.group(2).strip()
        await qr_logic(message, texte)
        return

    # Bombe: "Nexus lance la bombe" ou "Nexus fais péter"
    if "nexus lance la bombe" in content or "nexus fais péter" in content:
        await bombe_logic(message)
        return

    # Température: "Nexus donne la température à [ville]" ou "Nexus météo [ville]"
    match = re.search(r"nexus (donne la température à|météo) (.+)", content)
    if match:
        ville = match.group(2).strip()
        await temperature_logic(message, ville)
        return

    # Respiration: "Nexus lance un exercice de respiration" ou "Nexus aide-moi à respirer"
    if "nexus lance un exercice de respiration" in content or "nexus aide-moi à respirer" in content:
        await respiration_exercice_logic(message)
        return

    # Radio: "Nexus joue la radio [nom de la radio]" ou "Nexus met la radio [nom de la radio]"
    match = re.search(r"nexus (joue la radio|met la radio) (.+)", content)
    if match:
        radio_name = match.group(2).strip()
        await radio_logic(message, radio_name)
        return

    # Serveurs: "Nexus montre les serveurs" ou "Nexus donne les infos serveurs"
    if "nexus montre les serveurs" in content or "nexus donne les infos serveurs" in content:
        await serveurs_logic(message)
        return

    # 8ball: "Nexus 8ball [question]" ou "Nexus réponds à [question]"
    match = re.search(r"nexus (8ball|réponds à) (.+)", content)
    if match:
        question = match.group(2).strip()
        await eightball_logic(message, question)
        return

    # Devine: "Nexus devine [nombre]"
    match = re.search(r"nexus devine (\d+)", content)
    if match:
        nombre = int(match.group(1))
        await devine_logic(message, nombre)
        return

    # Pile ou Face: "Nexus pile ou face"
    if "nexus pile ou face" in content:
        await pileface_logic(message)
        return

    # Chifoumi: "Nexus pierre feuille ciseaux [ton choix]" ou "Nexus joue chifoumi [ton choix]"
    match = re.search(r"nexus (pierre feuille ciseaux|joue chifoumi) (pierre|feuille|ciseaux)", content)
    if match:
        choix = match.group(2).strip()
        await chifoumi_logic(message, choix)
        return

    # Salon privé temporaire: "Nexus crée un salon privé temporaire [nom du salon]"
    match = re.search(r"nexus crée un salon privé temporaire (.+)", content)
    if match:
        nom_salon = match.group(1).strip()
        await salon_prive_temporaire_logic(message, nom_salon)
        return

    # Ajouter membre salon: "Nexus ajoute @membre au salon [ID du salon]"
    match = re.search(r"nexus ajoute (.+) au salon (\d+)", content)
    if match:
        member_name = match.group(1).strip()
        salon_id = int(match.group(2))
        member = await find_member_by_name(message.guild, member_name)
        if member:
            await ajouter_membre_salon_logic(message, salon_id, member)
        else:
            await message.reply("❌ Nexus n'a pas pu trouver ce membre. Assurez-vous de le mentionner ou d'écrire son nom correctement.")
        return

    # --- Réponses génériques (si aucune commande n'est détectée) ---

    salutations = ["salut", "bonjour", "coucou", "hola", "hello", "bonsoir", "slt", "bjr"]
    depart = ["au revoir", "bye", "a+", "ciao", "see ya", "à bientôt", "adieu", "bonne nuit", "bn", "tchao"]
    faim = ["j'ai faim", "faim", "j’ai la dalle", "je crève de faim", "trop faim", "je crève la dalle"]
    quoifeur = ["quoi"]
    cava = ["ca va?", "cv?", "ça va ?", "bien ou bien"]
    caca = ["caca", "crotte"]
    rigole = ["haha", "lol", "mdr", "ptdr"]
    musique = ["musique", "chanson", "playlist", "écouter", "chant"]
    triste = ["triste", "déprimé", "mélancolique", "morose"]

    if any(word in content for word in salutations):
        await message.reply(f"Salut {message.author.mention} !")
        return
    elif any(word in content for word in depart):
        await message.reply(f"Bye {message.author.mention} !")
        return
    elif any(word in content for word in faim):
        await message.reply("Tiens une bonne assiette de pâtes carbonara :\nhttps://cdn.pixabay.com/photo/2011/04/29/11/20/spaghetti-7113_1280.jpg")
        return
    elif any(word in content for word in quoifeur):
        await message.reply("Feur ! Hahahahaha très drôle nan ? ")
        return
    elif any(word in content for word in cava):
        await message.reply("Je ne peux aller ni mal ni bien, vu que je ne suis qu'un bot... Mais toi, ça va ?")
        return
    elif any(word in content for word in caca):
        embed = discord.Embed()
        embed.set_image(url="https://cdn.pixabay.com/photo/2014/02/13/11/56/wc-265278_1280.jpg")
        await message.reply(embed=embed)
        return
    elif any(word in content for word in rigole):
        await message.reply("Dommage que je ne puisse pas rire comme toi...")
        return
    elif any(word in content for word in musique):
        await message.reply("Moi je connais une superbe chanson... Never gonna give you up, never gonna let you down, Never gonna run around and desert you, Never gonna make you cry, never gonna say goodbye Never gonna tell a lie and hurt you ! ")
        return
    elif any(word in content for word in triste):
        await message.reply("Nexus te conseille de lui demander de raconter une blague pour te remonter le moral nan ?")
        return
    
    # Vérifier si le bot est mentionné spécifiquement (après les commandes pour éviter les conflits)
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if len(message.mentions) == 1 and message.mentions[0] == bot.user:
            embed = discord.Embed(
                title="Je suis Nexus Bot",
                description="Un bot open source par CF Games",
                color=discord.Color.blue()
            )
            await message.channel.send(embed=embed)


# Cette fonction est maintenant la porte d'entrée pour configurer le bot
def setup_bot():
    """
    Configure le bot pour l'importation.
    Retourne l'instance du bot.
    """
    
    return bot

