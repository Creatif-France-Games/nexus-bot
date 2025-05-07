import discord
from discord.ext import commands
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Chargement du modèle avec prise en charge du format "chat"
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1", trust_remote_code=True)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, trust_remote_code=True)

def ask_deepseek(user_prompt):
    messages = [{"role": "user", "content": user_prompt}]
    output = pipe(messages, max_new_tokens=200, do_sample=True, temperature=0.7)
    return output[0]["generated_text"]

def setup(bot):
    @bot.command(name="deepseek")
    async def deepseek_command(ctx, *, prompt):
        await ctx.defer()
        reply = ask_deepseek(prompt)
        await ctx.send(reply[:2000])  # 2000 caractères max
