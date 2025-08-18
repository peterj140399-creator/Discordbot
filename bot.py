import os
import discord
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_ID = int(os.getenv("WEBHOOK_ID"))  # ID numérica del webhook

# Intents necesarios
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

    # Solo responder a mensajes del webhook
    if message.webhook_id != WEBHOOK_ID:
        return

    # Determinar tipo de hilo según contenido del mensaje
    content = message.content
    if "¿Qué sugerencia tienes para nosotros?" in content:
        thread_name = "Sugerencia"
    elif "¿Sobre quién quieres hablarnos?" in content:
        thread_name = "Reporte"
    else:
        thread_name = "General"

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
