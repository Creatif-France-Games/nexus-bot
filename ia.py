import discord
from discord.ext import commands
import aiohttp
import os
import io

# --- Configuration du Cog ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "google/gemma-3n-e2b-it:free"  # Modèle mis à jour
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class IACog(commands.Cog):
    """
    Cog pour la commande /ia qui interagit avec OpenRouter.ai
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not OPENROUTER_API_KEY:
            print("N E X U S B O T - ⚠️ ATTENTION : Clé API OpenRouter non configurée.")

    @discord.app_commands.command(name="ia", description="Discutez avec l'IA Gemma 3n E2B IT (Google, via OpenRouter)")
    @discord.app_commands.describe(
        prompt="La question ou requête à envoyer à l'IA"
    )
    async def ia_command(self, interaction: discord.Interaction, prompt: str):
        """
        Envoie le prompt à OpenRouter et retourne la réponse.
        """
        if not OPENROUTER_API_KEY:
            await interaction.response.send_message(
                "❌ Erreur : Clé API OpenRouter non configurée.",
                ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/Creatif-France-Games/nexus-bot",  # URL valide
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(OPENROUTER_API_URL, json=payload) as response:
                    raw_text = await response.text()

                    if response.status != 200:
                        await interaction.followup.send(
                            f"❌ Erreur API OpenRouter ({response.status}) :\n```\n{raw_text}\n```"
                        )
                        return

                    data = await response.json()

            # Extraction sécurisée de la réponse IA
            choice = data.get("choices", [{}])[0]
            ai_response = (
                choice.get("message", {}).get("content") or
                choice.get("text") or
                "❌ Aucune réponse reçue."
            )

            # Gestion si réponse trop longue pour Discord
            if len(ai_response) > 1990:
                file = discord.File(
                    io.BytesIO(ai_response.encode("utf-8")),
                    filename="reponse.txt"
                )
                await interaction.followup.send(
                    content=f"**Question :** {prompt}\n\nRéponse trop longue, voir fichier ci-joint :",
                    file=file
                )
            else:
                await interaction.followup.send(
                    f"**Question :** {prompt}\n\n**Réponse de l'IA :** {ai_response}"
                )

        except aiohttp.ClientError as e:
            await interaction.followup.send(f"❌ Erreur de connexion : {e}")

        except Exception as e:
            await interaction.followup.send(f"❌ Erreur inattendue : {e}")

# Fonction de setup du cog
async def setup(bot: commands.Bot):
    await bot.add_cog(IACog(bot))
