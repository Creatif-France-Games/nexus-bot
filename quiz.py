import discord
from discord.ext import commands
from discord import app_commands

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = {}  # user_id -> {"q": ..., "r": ..., "asked_by": ...}

    @app_commands.command(name="quiz", description="Pose une question aux membres du salon.")
    @app_commands.describe(question="La question à poser", reponse="La réponse attendue")
    async def quiz(self, interaction: discord.Interaction, question: str, reponse: str):
        self.active[interaction.channel_id] = {
            "q": question,
            "r": reponse.lower(),
            "asked_by": interaction.user.display_name
        }
        await interaction.response.send_message(
            f"📢 **Question posée par {interaction.user.mention} :**\n{question}\nRépondez avec `/repondre <ta_réponse>`"
        )

    @app_commands.command(name="repondre", description="Réponds à la question active dans le salon")
    @app_commands.describe(ta_reponse="Ta réponse")
    async def repond(self, interaction: discord.Interaction, ta_reponse: str):
        q = self.active.get(interaction.channel_id)
        if not q:
            await interaction.response.send_message("❌ Aucune question active dans ce salon.")
            return
        if ta_reponse.lower() == q["r"]:
            await interaction.response.send_message(f"✅ Bonne réponse, {interaction.user.mention} !")
        else:
            await interaction.response.send_message(f"❌ Mauvaise réponse, {interaction.user.mention}.")

# Retirer l'await ici, juste un appel classique
def setup(bot):
    bot.add_cog(Quiz(bot))
