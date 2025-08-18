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

# Aquí pon el ID de tu webhook si quieres filtrar solo sus mensajes
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
        # Intentar extraer el nick de la primera pregunta del Google Form
        nick = "desconocido"
        for line in message.content.split("\n"):
            if line.startswith("Nick en el servidor:"):
                nick = line.replace("Nick en el servidor:", "").strip()
                break

        # Crear hilo en el canal del mensaje
        thread_name = f"Sugerencia de {nick}"
        try:
            await message.channel.create_thread(
                name=thread_name,
                message=message,
                type=discord.ChannelType.public_thread  # hilo público
            )
            print(f"Hilo '{thread_name}' creado.")
        except Exception as e:
            print(f"Error creando hilo: {e}")

# Ejecutar el bot
client.run(TOKEN)
