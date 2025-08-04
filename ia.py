import discord
from discord.ext import commands
import aiohttp
import os

# --- Configuration du Cog ---
# La clé API et le modèle sont définis ici pour ce module.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "openrouter/horizon-beta"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class IACog(commands.Cog):
    """
    Ce cog gère la commande slash /ia pour interagir avec OpenRouter.ai.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Assurez-vous que les clés sont définies
        if not OPENROUTER_API_KEY:
            print("ATTENTION: La clé API OpenRouter n'est pas configurée.")

    @discord.app_commands.command(name="ia", description="Discutez avec le modèle d'IA Horizon Beta")
    @discord.app_commands.describe(
        prompt="La question ou la requête à envoyer à l'IA"
    )
    async def ia_command(self, interaction: discord.Interaction, prompt: str):
        """
        Cette commande slash envoie une requête à l'API d'OpenRouter et renvoie la réponse.
        """
        # Vérifie si la clé API est disponible avant de continuer
        if not OPENROUTER_API_KEY:
            await interaction.response.send_message("❌ Erreur : La clé API OpenRouter n'est pas configurée sur le bot.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        async with aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "Votre Application Discord",  # Remplacez par le nom de votre app
                "Content-Type": "application/json"
            }
        ) as session:
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            try:
                async with session.post(OPENROUTER_API_URL, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if data and 'choices' in data and len(data['choices']) > 0:
                        ai_response = data['choices'][0]['message']['content']
                        await interaction.followup.send(f"**Question:** {prompt}\n\n**Réponse de l'IA:** {ai_response}")
                    else:
                        await interaction.followup.send("❌ Erreur : Je n'ai pas pu obtenir de réponse de l'IA.")

            except aiohttp.ClientError as e:
                await interaction.followup.send(f"❌ Erreur de connexion : {e}")
            except Exception as e:
                await interaction.followup.send(f"❌ Une erreur inattendue est survenue : {e}")

# Cette fonction est obligatoire pour que le fichier soit un cog.
# Elle est appelée par le bot principal pour charger ce module.
async def setup(bot: commands.Bot):
    """
    Ajoute le cog au bot.
    """
    await bot.add_cog(IACog(bot))
