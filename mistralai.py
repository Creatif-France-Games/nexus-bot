import discord
from discord.ext import commands  # Assure-toi que cette ligne est bien présente
from discord import app_commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B"

class MistralAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mistral", description="Pose une question à Mistral AI")
    async def mistral(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        data = {"inputs": prompt}

        try:
            response = requests.post(API_URL, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                reply = result["generated_text"][:2000]  # Limite à 2000 caractères
                await interaction.followup.send(reply)
            else:
                await interaction.followup.send(f"Erreur {response.status_code} : {response.text}")
        except Exception as e:
            await interaction.followup.send(f"Erreur : {str(e)}")

async def setup(bot):
    await bot.add_cog(MistralAI(bot))


