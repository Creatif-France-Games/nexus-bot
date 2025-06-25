from discord.ext import commands
import difflib

def setup(bot: commands.Bot):
    command_phrases = {
        'de': [
            "lance un dé", "lancer un dé", "lance une de", "lance un de",
            "lance un dé stp", "lancer une dé", "lancer un dé stp"
        ],
        'compliment': [
            "fais un compliment", "dis un compliment", "complimente-moi"
        ],
        'ping': [
            "ping", "teste la latence"
        ],
        'infobot': [
            "informe moi", "info bot", "donne des infos"
        ],
        'avatar': [
            "montre mon avatar", "affiche avatar"
        ],
        'temperature': [
            "quelle est la température", "donne la température"
        ],
        'blague': [
            "raconte une blague", "blague", "fais rire"
        ],
        '8ball': [
            "8ball", "boule magique", "pose une question"
        ],
        'devine': [
            "joue à devine", "devine"
        ],
        'pileface': [
            "pile ou face", "joue à pile face", "pileface"
        ],
        'chifoumi': [
            "joue à chifoumi", "pierre feuille ciseaux", "chifoumi"
        ],
    }

    SIMILARITY_THRESHOLD = 0.6

    @bot.event
    async def on_message(message):
        # Ignore les messages des bots
        if message.author.bot:
            return

        msg = message.content.lower()

        # Recherche d'une commande similaire
        for command_name, phrases in command_phrases.items():
            for phrase in phrases:
                ratio = difflib.SequenceMatcher(None, msg, phrase).ratio()
                if ratio >= SIMILARITY_THRESHOLD:
                    ctx = await bot.get_context(message)
                    command = bot.get_command(command_name)
                    if command:
                        await command.invoke(ctx)
                    else:
                        print(f"Commande '{command_name}' non trouvée.")
                    return  # Stop après la première commande trouvée

        # Laisse la gestion aux commandes classiques si rien n'a été reconnu
        await bot.process_commands(message)
