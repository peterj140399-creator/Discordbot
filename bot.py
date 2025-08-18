import os
import discord
from dotenv import load_dotenv

# Cargar token desde environment
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

    # Solo procesar mensajes de nuestro webhook
    if message.webhook_id != WEBHOOK_ID:
        return

    # Intentar extraer el nick desde el contenido
    nick = "desconocido"
    try:
        lines = [line.strip() for line in message.content.splitlines() if line.strip()]
        for i, line in enumerate(lines):
            if line.lower() == "nick en el servidor" and i+1 < len(lines):
                nick = lines[i+1]
                break
    except Exception as e:
        print(f"Error al extraer nick: {e}")

    # Crear hilo
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
