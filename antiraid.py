# Codé par GPT et Team CF Games
import discord
from discord.ext import commands, tasks
import asyncio
from collections import defaultdict
import time

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg_times = defaultdict(list)  # user_id -> list of msg timestamps
        self.join_times = []
        self.securising = False
        self.security_channel_id = 1281639179331043382

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        now = time.time()
        times = self.msg_times[message.author.id]

        # Supprime les timestamps trop vieux (genre +20s)
        self.msg_times[message.author.id] = [t for t in times if now - t < 20]
        self.msg_times[message.author.id].append(now)

        # Check si le user envoie un message toutes les 1s
        if len(self.msg_times[message.author.id]) >= 2:
            if self.msg_times[message.author.id][-1] - self.msg_times[message.author.id][-0.9] < 2:
                try:
                    await message.delete()
                except:
                    pass

                channel = self.bot.get_channel(self.security_channel_id)
                if channel:
                    embed = discord.Embed(
                        description="🔒 Nexus Bot à protégé ce serveur.\nUn bot/un profil à spammé les messages, ils ont été supprimés.",
                        color=0xFF0000
                    )
                    await channel.send(embed=embed)

                # Lance sécurisation si pas déjà lancé
                if not self.securising:
                    await self.start_securisation()
                return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = time.time()
        self.join_times.append(now)

        # Garder que les joins des 3 dernières secondes
        self.join_times = [t for t in self.join_times if now - t < 3]

        if len(self.join_times) >= 5 and not self.securising:
            await self.start_securisation()

    async def start_securisation(self):
        self.securising = True
        channel = self.bot.get_channel(self.security_channel_id)
        if not channel:
            return

        # Message début sécurisation
        embed_start = discord.Embed(
            description="⚠️ Une possible cyberattaque envers le serveur à été détectée.\nPar mesure de sécurité, le serveur est en mode sécurité. Merci de votre compréhension",
            color=0xFFA500
        )
        await channel.send(embed=embed_start)

        # Bloquer les permissions dans tous les channels texte et threads
        overwrite = discord.PermissionOverwrite(send_messages=False, create_public_threads=False, create_private_threads=False)
        for guild in self.bot.guilds:
            for ch in guild.text_channels + guild.threads:
                try:
                    await ch.set_permissions(guild.default_role, overwrite=overwrite)
                except:
                    pass

        # Attendre 20 minutes
        await asyncio.sleep(20 * 60)

        # Enlever le blocage
        for guild in self.bot.guilds:
            for ch in guild.text_channels + guild.threads:
                try:
                    await ch.set_permissions(guild.default_role, overwrite=None)
                except:
                    pass

        # Message fin sécurisation
        embed_end = discord.Embed(
            description="✅ La sécurisation est terminée, merci de votre compréhension",
            color=0x00FF00
        )
        await channel.send(embed=embed_end)
        self.securising = False


async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
