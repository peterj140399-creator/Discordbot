import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    print("==== NUEVO MENSAJE RECIBIDO ====")
    print(f"Author: {message.author}")
    print(f"Webhook ID: {message.webhook_id}")
    print(f"Content: {message.content}")
    print(f"Embeds: {message.embeds}")

client.run(TOKEN)
