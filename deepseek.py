import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1"

class DeepSeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="deepseek", description="Pose une question à DeepSeek")
    async def deepseek(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        data = {"inputs": [{"role": "user", "content": prompt}]}
        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            reply = result[0]["generated_text"][:2000]
            await interaction.followup.send(reply)
        else:
            await interaction.followup.send("Erreur : impossible de récupérer une réponse.")

async def setup(bot):
    await bot.add_cog(DeepSeek(bot))

