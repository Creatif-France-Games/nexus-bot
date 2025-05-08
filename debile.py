import discord
from discord.ext import commands
import random

# Contenus des catégories
sujets = [
    "Un développeur", "Un robot stalinien", "Une licorne sous caféine", "Chuck Norris", "Un bug cosmique", 
    "Un parseur XML", "Le stagiaire en crise", "Un pigeon schizophrène", "Une imprimante démoniaque", 
    "Un kangourou freelance", "Un codeur avec 2h de sommeil", "Un ninja sous Red Bull", "Un serveur AWS tombé", 
    "Un stagiaire avec 3 ans de retard", "Un chat qui fait du Python", "Un hamster avec un disque dur SSD", 
    "Un hérisson en train de coder", "Un alien avec un PC portable", "Un piéton qui compile son code", 
    "Un développeur d’extension Chrome", "Un serveur de dev en pannes", "Un panda ninja", "Chuck Norris", 
    "Une mouette en colère", "Un alien confus", "Un dragon sur un skateboard", "Un hamster armé", 
    "Un super-héros dépressif", "Un zombie végétarien", "Un robot qui a oublié de recharger", 
    "Un clown en pleine crise existentielle", "Un arbre qui a perdu ses feuilles", "Une licorne en vacances", 
    "Un vampire vegan", "Un chat qui croit qu'il est un chien", "Une girafe qui danse la salsa", "Un cheval qui fait du yoga", 
    "Chuck Norris"
]

actions = [
    "mange", "hésite devant", "regarde de travers", "fait un backflip sur", "utilise", "hacke", "supprime", 
    "slappe", "déploie", "tape du pied sur", "débogue", "pousse sans raison", "compile", "reverse-engineer", 
    "télécharge", "ignore totalement", "ferme en mode ninja", "improvise", "tape un code magique sur", "fait un moonwalk", 
    "prend une douche froide", "saute à l’élastique", "part en voyage dans le temps", "se déclare à un cactus", 
    "pousse un cri effrayant", "chante l'hymne national en version rap", "combat un dragon avec une baguette de pain", 
    "boit du café avec des lunettes de soleil", "démarre une guerre de coussins", "se transforme en licorne", 
    "cherche des clés invisibles", "se cache sous une table", "fais un backflip en atterrissant sur une pizza", 
    "explore l'univers avec un tuba", "défie Chuck Norris dans un duel de regards"
]

objets = [
    "une pizza radioactive", "le code source du bot", "un commit foireux", "un terminal maudit", "un bug cosmique", 
    "la RAM du serveur", "un parseur XML", "un docker possédé", "une IA qui pleure", "un clavier QWERTY", 
    "le café du dev", "la dignité du frontend", "le terminal bleu de la mort", "un container Docker fou", 
    "le mot de passe en clair", "un script Python qui parle", "un fichier `.env` effacé", "le disque dur cassé", 
    "le Wi-Fi de l’open-space", "le code legacy de 2009", "une requête SQL mal formée", "le PC du collège", 
    "un Windows 11", "un PC commandé sur Wish", "un rouleau de papier toilette magique", "une pizza qui vole", 
    "un casque de réalité virtuelle défectueux", "une baguette magique cassée", "un parapluie inversé", 
    "une raquette de ping-pong géante", "un pogo stick avec un moteur de fusée", "une chaise qui roule toute seule", 
    "un téléphone avec une mauvaise connexion", "un ballon qui parle", "un sabre laser en mousse", "une montre qui ne donne jamais l'heure", 
    "un pistolet à eau géant", "une boîte de céréales sans céréales", "un gobelet à café rempli de gelée", "un smartphone qui fait des blagues"
]

punchlines = [
    "et Git n'a rien pu faire.", "même Chuck Norris a tapé la fuite.", "et VSCode a crashé de honte.", 
    "du coup Jenkins a démissionné.", "puis tout Internet a rebooté.", "et depuis, c’est une feature.", 
    "parce que pourquoi pas.", "et personne n’en parle encore aujourd’hui.", "et les serveurs AWS sont tombés.", 
    "en sifflant l’hymne de Linux.", "et tout a été réécrit en Ruby.", "et ça a brisé l'espace-temps.", "et je suis en train de rollback.", 
    "et Docker est en mode Safe Mode.", "les devs ont pleuré.", "tout le code a disparu dans une faille spatio-temporelle.", 
    "et même StackOverflow a crashé.", "et le serveur a pris un 503 pour Noël.", "puis l'équipe a sombré dans l'oubli.", 
    "et le frontend a fait une crise de panique.", "même Chuck Norris n'a pas compris", "et Chuck Norris a encore gagné.", 
    "et depuis, la Terre a arrêté de tourner par respect.", "et tout le monde a eu un congé maladie.", "et le Wi-Fi est devenu plus rapide.", 
    "et les aliens ont quitté la galaxie en courant.", "et l'univers a redémarré pour le rendre possible.", 
    "et la gravité a décidé de prendre une pause.", "et c'était le début de la fin... ou peut-être juste une pause.", 
    "et tout est devenu un meme instantanément.", "et personne n'ose le défier à nouveau.", "et Chuck Norris a encore fait un uppercut à la physique.", 
    "et un singe en a fait un TikTok.", "et tous les serveurs ont planté de honte.", "et les dinosaures sont venus demander des conseils.", 
    "et Chuck Norris est parti en courant."
]

# Commande /debile
async def debile(interaction: discord.Interaction):
    # Générer une phrase aléatoire à partir des listes
    phrase = f"🧠 {random.choice(sujets)} {random.choice(actions)} {random.choice(objets)}... {random.choice(punchlines)}"
    
    # Envoyer la phrase générée
    await interaction.response.send_message(phrase)

# Configuration de la commande
def setup(bot):
    @bot.tree.command(name="debile", description="Génère une phrase complètement débile", guild_ids=[1281639178689319067])
    async def debile_command(interaction: discord.Interaction):
        await debile(interaction)
