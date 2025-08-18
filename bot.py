import os
import discord
from dotenv import load_dotenv

# Cargar token desde environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_ID = int(os.getenv("WEBHOOK_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Solo mensajes del webhook
    if message.webhook_id != WEBHOOK_ID:
        return

    nick = "desconocido"

    # Revisar embeds
    if message.embeds:
        embed = message.embeds[0]
        if embed.description:
            lines = [line.strip() for line in embed.description.splitlines() if line.strip()]
            for i, line in enumerate(lines):
                if line.lower() == "nick en el servidor" and i + 1 < len(lines):
                    nick = lines[i + 1]
                    break

    thread_name = f"Sugerencia de {nick}"
    try:
        await message.channel.create_thread(
            name=thread_name,
            message=message,
            type=discord.ChannelType.public_thread
        )
        print(f"Hilo '{thread_name}' creado.")
    except Exception as e:
        print(f"Error creando hilo: {e}")

client.run(TOKEN)
