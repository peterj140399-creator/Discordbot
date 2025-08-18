import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

WEBHOOK_ID = 1406962453987725392  # tu webhook real

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.webhook_id == WEBHOOK_ID:
        nick = "desconocido"
        try:
            description = message.embeds[0].description
            for line in description.splitlines():
                if line.lower().startswith("nick en el servidor"):
                    # línea como "Nick en el servidor\nNickReal"
                    parts = line.split("\n")
                    if len(parts) == 2:
                        nick = parts[1].strip()
                    else:
                        nick = line.split(":")[-1].strip()  # fallback
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
