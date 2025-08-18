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
    if message.author == client.user:
        return

    # Solo reaccionar a mensajes del webhook
    if message.webhook_id != WEBHOOK_ID:
        return

    # Mostrar todo el mensaje para depuración
    print("=== Nuevo mensaje del webhook ===")
    print(f"Contenido: {message.content}")
    print(f"Embeds: {message.embeds}")

    # Intentar extraer nick del contenido
    nick = "desconocido"
    if "Sugerencia enviada por" in message.content:
        try:
            # Tomar lo que esté entre "Sugerencia enviada por" y ":mailbox"
            nick = message.content.split("Sugerencia enviada por")[1].split(":mailbox")[0].strip()
        except Exception:
            pass
    # Si no, intentar desde embed
    elif message.embeds:
        embed = message.embeds[0]
        if embed.description:
            lines = embed.description.splitlines()
            if lines:
                nick = lines[0].strip()  # usualmente la primera línea del embed

    thread_name = f"Sugerencia de {nick}"

    try:
        await message.channel.create_thread(
            name=thread_name,
            message=message,
            type=discord.ChannelType.public_thread
        )
        print(f"Hilo '{thread_name}' creado correctamente.")
    except Exception as e:
        print(f"Error creando hilo: {e}")

client.run(TOKEN)
