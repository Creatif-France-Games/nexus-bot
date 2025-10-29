import discord  
from discord.ext import commands  
import aiohttp  
import os  
import io  
  
# --- Configuration du Cog ---  
  
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  
MODEL_NAME = "google/gemma-3n-e2b-it:free"  # Modèle mis à jour  
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"  
  
# Prompt système pour la commande Minetest  
  
MINETEST_SYSTEM_PROMPT = (  
    "Tu dois générer le code d’un mod Minetest complet et fonctionnel à partir de la description donnée.  
Suis strictement ces instructions :Utilise uniquement l’API officielle de Minetest (minetest.register_*),Le code doit être compatible avec les versions récentes de Minetest,Le fichier principal doit s’appeler init.lua,ne crée pas de fonctions ou classes inutiles (comme on_load, create_command, etc.),Ne renvoie aucun texte explicatif ni commentaire hors du code,Ne formate pas la réponse en Markdown, renvoie uniquement le code brut,n'hésite pas a ajouter des commentaires pour expliquer ton code.Ton rôle : produire uniquement le contenu exact du mod."  
)  
  
class IACog(commands.Cog):  
    """  
    Cog pour la commande /ia qui interagit avec OpenRouter.ai  
    et pour la commande /generer-minetest-mod qui demande à l'IA de générer  
    exclusivement le code d'un mod Minetest.  
    """  
    def __init__(self, bot: commands.Bot):  
        self.bot = bot  
        if not OPENROUTER_API_KEY:  
            print("N E X U S B O T - ⚠️ ATTENTION : Clé API OpenRouter non configurée.")  
  
    async def _call_openrouter(self, messages):    
        """    
        Appelle l'API OpenRouter avec la liste de messages fournie.    
        Renvoie la réponse texte de l'IA.    
        Lève une exception en cas d'erreur d'API ou de connexion.    
        """    
        headers = {    
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",    
            "HTTP-Referer": "https://github.com/Creatif-France-Games/nexus-bot",    
            "Content-Type": "application/json"    
        }    
  
        payload = {    
            "model": MODEL_NAME,    
            "messages": messages,    
            "temperature": 0.7    
        }    
  
        async with aiohttp.ClientSession(headers=headers) as session:    
            async with session.post(OPENROUTER_API_URL, json=payload) as response:    
                raw_text = await response.text()    
  
                if response.status != 200:    
                    raise RuntimeError(f"Erreur API OpenRouter ({response.status}) :\n{raw_text}")    
  
                data = await response.json()    
  
        choice = data.get("choices", [{}])[0]    
        ai_response = (    
            choice.get("message", {}).get("content")    
            or choice.get("text")    
            or "❌ Aucune réponse reçue."    
        )    
  
        return ai_response    
  
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
  
        try:    
            messages = [    
                {"role": "user", "content": prompt}    
            ]    
            ai_response = await self._call_openrouter(messages)    
  
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
  
    @discord.app_commands.command(    
        name="generer-minetest-mod",    
        description="Génère le code d'un mod Minetest via l'IA. L'IA renverra uniquement le code du mod."    
    )    
    @discord.app_commands.describe(    
        description="Décrivez le mod Minetest à générer (fonctionnalités, fichiers attendus, etc.)"    
    )    
    async def generer_minetest_mod(self, interaction: discord.Interaction, description: str):    
        """    
        Envoie à l'IA la description fournie par l'utilisateur ainsi qu'un prompt système    
        qui ordonne de ne renvoyer que le code du mod Minetest.    
        """    
        if not OPENROUTER_API_KEY:    
            await interaction.response.send_message(    
                "❌ Erreur : Clé API OpenRouter non configurée.",    
                ephemeral=True    
            )    
            return    
  
        await interaction.response.defer(thinking=True)    
  
        try:    
            messages = [
    {"role": "user", "content": f"{MINETEST_SYSTEM_PROMPT}\n\n{description}"}
]
            ai_response = await self._call_openrouter(messages)    
  
            # La commande attend en pratique du code ; on renvoie tel quel.    
            # S'il est trop long, on envoie en pièce jointe.    
            if len(ai_response) > 1990:    
                file = discord.File(    
                    io.BytesIO(ai_response.encode("utf-8")),    
                    filename="mod_minetest_code.txt"    
                )    
                await interaction.followup.send(    
                    content=f"**Description :** {description}\n\nLe code est trop long, voir fichier ci-joint :",    
                    file=file    
                )    
            else:    
                # Pour la commande Minetest, on renvoie simplement le code reçu.    
                await interaction.followup.send(    
                    f"**Description :** {description}\n\n**Code du mod Minetest :**\n{ai_response}"    
                )    
  
        except aiohttp.ClientError as e:    
            await interaction.followup.send(f"❌ Erreur de connexion : {e}")    
  
        except Exception as e:    
            await interaction.followup.send(f"❌ Erreur inattendue : {e}")  
  
# Fonction de setup du cog  
  
async def setup(bot: commands.Bot):  
    await bot.add_cog(IACog(bot))