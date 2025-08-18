import os
import discord
from dotenv import load_dotenv

# Cargar token desde environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_ID = int(os.getenv("WEBHOOK_ID"))  # Asegúrate de que esté en environment

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

    # Solo procesar mensajes del webhook específico
    if message.webhook_id == WEBHOOK_ID:
        nick = "desconocido"

        # Revisar embeds
        if message.embeds:
            embed = message.embeds[0]
            if embed.description:
                lines = embed.description.splitlines()
                try:
                    # Buscar la línea "Nick en el servidor" y tomar la siguiente como nick
                    index = lines.index("Nick en el servidor")
                    nick = lines[index + 1].strip()
                except (ValueError, IndexError):
                    pass

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
