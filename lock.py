import discord
from discord.ext import commands
from discord import app_commands

@bot.tree.command(name="verrouiller", description="Verrouille un salon.")
async def verrouiller(interaction: discord.Interaction, channel: discord.TextChannel, duration: str = None, reason: str = "Ce salon est verrouillé."):
    # check permissions à la main
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("T'as pas la permission de gérer les salons.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    default_role = interaction.guild.default_role
    perms = channel.overwrites_for(default_role)
    perms.send_messages = False
    await channel.set_permissions(default_role, overwrite=perms)

    old_name = channel.name
    await channel.edit(name=f"🔒-{old_name}")

    msg = await channel.send(f"🔒 SALON VERROUILLÉ 🔒\n{reason}\nVerrouillé par {interaction.user.mention}")

    if not hasattr(bot, 'locked_channels'):
        bot.locked_channels = {}
    bot.locked_channels[channel.id] = {
        "old_name": old_name,
        "lock_msg_id": msg.id,
        "old_perms": perms
    }

    await interaction.followup.send(f"{channel.mention} est verrouillé.", ephemeral=True)

    if duration:
        unit = duration[-1]
        try:
            val = int(duration[:-1])
        except:
            return await interaction.followup.send("Durée invalide, format: 30s, 10m, 1h.", ephemeral=True)

        seconds = {'s':1, 'm':60, 'h':3600}.get(unit)
        if not seconds:
            return await interaction.followup.send("Unitée invalide, utilise s, m ou h.", ephemeral=True)
        await asyncio.sleep(val * seconds)

        if channel.id in bot.locked_channels:
            await deverrouiller_logic(channel, interaction.guild.default_role, bot.locked_channels[channel.id])
            await channel.send(f"{channel.mention} a été déverrouillé automatiquement après {duration}.")
            del bot.locked_channels[channel.id]

@bot.tree.command(name="deverrouiller", description="Déverrouille un salon.")
async def deverrouiller(interaction: discord.Interaction, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("T'as pas la permission de gérer les salons.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    if not hasattr(bot, 'locked_channels') or channel.id not in bot.locked_channels:
        return await interaction.followup.send(f"{channel.mention} n'est pas verrouillé par cette commande.", ephemeral=True)

    await deverrouiller_logic(channel, interaction.guild.default_role, bot.locked_channels[channel.id])
    del bot.locked_channels[channel.id]
    await interaction.followup.send(f"{channel.mention} est déverrouillé.", ephemeral=True)

async def deverrouiller_logic(channel, default_role, lock_info):
    await channel.set_permissions(default_role, overwrite=lock_info["old_perms"])
    await channel.edit(name=lock_info["old_name"])

    try:
        msg = await channel.fetch_message(lock_info["lock_msg_id"])
        await msg.delete()
    except discord.NotFound:
        pass

