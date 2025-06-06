import discord
from discord import app_commands
from discord.ext import commands
import asyncio

@bot.tree.command(name="verrouiller", description="Verrouille un salon.")
@app_commands.describe(
    channel="Le salon à verrouiller.",
    duration="Durée du verrouillage (ex: 1h, 30m, 5s). Laissez vide pour un verrouillage permanent.",
    reason="Le message à afficher pour le verrouillage."
)
@app_commands.checks.has_permissions(manage_channels=True)
async def verrouiller(interaction: discord.Interaction, channel: discord.TextChannel, duration: str = None, reason: str = "Ce salon est actuellement verrouillé."):
    """Locks a channel, preventing non-admin users from sending messages."""
    await interaction.response.defer(ephemeral=True) # Defer the response as this might take a moment

    original_permissions = channel.overwrites_for[interaction.guild.default_role] if interaction.guild.default_role in channel.overwrites else None

    # Get the default role for the guild
    default_role = interaction.guild.default_role

    # Set permissions to deny sending messages for the default role
    perms = channel.overwrites_for[default_role]
    perms.send_messages = False
    await channel.set_permissions(default_role, overwrite=perms)

    # Add padlock emoji to the channel name
    original_channel_name = channel.name
    new_channel_name = f"🔒-{original_channel_name}"
    await channel.edit(name=new_channel_name)

    # Send the lock message
    lock_message = await channel.send(f"🔒 **SALON VERROUILLÉ** 🔒\n{reason}\n\n**Ce salon a été verrouillé par {interaction.user.mention}.**")

    # Store channel state for unlocking
    bot.locked_channels = getattr(bot, 'locked_channels', {})
    bot.locked_channels[channel.id] = {
        "original_name": original_channel_name,
        "lock_message_id": lock_message.id,
        "original_permissions": original_permissions # Store original permissions
    }

    await interaction.followup.send(f"Le salon {channel.mention} a été verrouillé.", ephemeral=True)

    if duration:
        time_unit = duration[-1]
        time_value = int(duration[:-1])

        if time_unit == 's':
            seconds = time_value
        elif time_unit == 'm':
            seconds = time_value * 60
        elif time_unit == 'h':
            seconds = time_value * 3600
        else:
            await interaction.followup.send("Durée non valide. Utilisez 's' pour secondes, 'm' pour minutes, 'h' pour heures (ex: 30m).", ephemeral=True)
            return

        await asyncio.sleep(seconds)
        # Automatically unlock after the specified duration
        if channel.id in bot.locked_channels: # Check if it's still locked
            await unlock_channel_logic(channel, interaction.guild.default_role, bot.locked_channels[channel.id]["original_name"], bot.locked_channels[channel.id]["original_permissions"], bot.locked_channels[channel.id]["lock_message_id"])
            await channel.send(f"Le salon {channel.mention} a été automatiquement déverrouillé après {duration}.")
            del bot.locked_channels[channel.id]

# --- Unlock Command ---
@bot.tree.command(name="deverrouiller", description="Déverrouille un salon.")
@app_commands.describe(channel="Le salon à déverrouiller.")
@app_commands.checks.has_permissions(manage_channels=True)
async def deverrouiller(interaction: discord.Interaction, channel: discord.TextChannel):
    """Unlocks a channel that was previously locked."""
    await interaction.response.defer(ephemeral=True)

    bot.locked_channels = getattr(bot, 'locked_channels', {})
    if channel.id not in bot.locked_channels:
        await interaction.followup.send(f"Le salon {channel.mention} n'est pas verrouillé par cette commande.", ephemeral=True)
        return

    original_name = bot.locked_channels[channel.id]["original_name"]
    lock_message_id = bot.locked_channels[channel.id]["lock_message_id"]
    original_permissions = bot.locked_channels[channel.id]["original_permissions"]

    await unlock_channel_logic(channel, interaction.guild.default_role, original_name, original_permissions, lock_message_id)

    del bot.locked_channels[channel.id]
    await interaction.followup.send(f"Le salon {channel.mention} a été déverrouillé.", ephemeral=True)

async def unlock_channel_logic(channel: discord.TextChannel, default_role: discord.Role, original_name: str, original_permissions: discord.PermissionOverwrite, lock_message_id: int):
    """Helper function to perform the unlocking logic."""
    # Restore original permissions or remove the overwrite if none existed
    if original_permissions:
        await channel.set_permissions(default_role, overwrite=original_permissions)
    else:
        await channel.set_permissions(default_role, overwrite=None) 

    # Remove padlock emoji from channel name
    await channel.edit(name=original_name)

    # Delete the lock message
    try:
        message = await channel.fetch_message(lock_message_id)
        await message.delete()
    except discord.NotFound:
        pass 
