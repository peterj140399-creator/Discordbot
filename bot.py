import os
import discord
from dotenv import load_dotenv

# Cargar token del archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# ID del webhook que quieres filtrar
WEBHOOK_ID = 1406962453987725392  # reemplaza con tu webhook real

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo responder si el mensaje viene del webhook
    if message.webhook_id == WEBHOOK_ID:
        nick = "desconocido"
        try:
            # Tomar la descripción del embed
            description = message.embeds[0].description
            # Buscar línea que contenga "Nick en el servidor"
            for line in description.splitlines():
                if "Nick en el servidor" in line:
                    nick = line.split(": ")[1].strip()
                    break
        except Exception as e:
            print(f"No se pudo obtener el nick: {e}")

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
