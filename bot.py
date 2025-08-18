import os
import discord
from dotenv import load_dotenv

# Cargar token del archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_ID = int(os.getenv("WEBHOOK_ID"))  # ID del webhook como número

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo responder si el mensaje viene del webhook específico
    if message.webhook_id == WEBHOOK_ID:
        thread_name = None

        # Revisamos los embeds para determinar si es sugerencia o reporte
        if message.embeds:
            embed = message.embeds[0]
            desc = embed.description.lower() if embed.description else ""

            if "qué sugerencia tienes para nosotros" in desc:
                thread_name = "Sugerencia"
            elif "sobre quién quieres hablarnos" in desc:
                thread_name = "Reporte"

        if thread_name:
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
