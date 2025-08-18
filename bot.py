import os
import discord
from dotenv import load_dotenv

# Cargar token del archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents necesarios para leer mensajes y crear threads
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# Nombre de tu webhook
WEBHOOK_NAME = "Buzón"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo responder si el mensaje viene del webhook con nombre "Buzón"
    if message.author.name != WEBHOOK_NAME:
        return

    # Tomar la primera línea del mensaje como nick
    nick = message.content.splitlines()[0].strip()
    if not nick:
        nick = "desconocido"

    thread_name = f"Sugerencia de {nick}"

    try:
        await message.channel.create_thread(
            name=thread_name,
            message=message,
            type=discord.ChannelType.public_thread  # público en el canal
        )
        print(f"Hilo '{thread_name}' creado.")
    except Exception as e:
        print(f"Error creando hilo: {e}")

# Ejecutar el bot
client.run(TOKEN)
