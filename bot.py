import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

WEBHOOK_ID = 1406962453987725392  # tu webhook

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.webhook_id == WEBHOOK_ID:
        # Extraer nombre desde el contenido del mensaje
        nick = "desconocido"
        for line in message.content.split("\n"):
            if line.startswith("Nick en el servidor:"):
                nick = line.replace("Nick en el servidor:", "").strip()
                break

        thread_name = f"Sugerencia de {nombre}"

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



