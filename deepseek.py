import discord
from discord.ext import commands
import requests

HF_TOKEN = "ton_token_hf"  # Token Hugging Face
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1"

def ask_deepseek(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {"inputs": [{"role": "user", "content": prompt}]}
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        return "Erreur, impossible de récupérer la réponse."

def setup(bot):
    @bot.command(name="deepseek")
    async def deepseek_command(ctx, *, prompt):
        await ctx.defer()
        reply = ask_deepseek(prompt)
        await ctx.send(reply[:2000])  # Limite Discord à 2000 caractères
