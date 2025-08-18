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

# ID del webhook del "Buzón"
WEBHOOK_ID = 1406962453987725392  # reemplaza con tu webhook real

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
        try:
            # Extraer el nick desde el embed
            if message.embeds:
                embed = message.embeds[0]
                # Cada línea del description es "Pregunta\nRespuesta"
                lines = embed.description.splitlines()
                nick = None
                for i in range(len(lines)-1):
                    question = lines[i].strip()
                    answer = lines[i+1].strip()
                    if question.lower() == "nick en el servidor":
                        nick = answer
                        break

                if not nick:
                    nick = "desconocido"

                thread_name = f"Sugerencia de {nick}"

                await message.channel.create_thread(
                    name=thread_name,
                    message=message,
                    type=discord.ChannelType.public_thread
                )
                print(f"Hilo '{thread_name}' creado.")

        except Exception as e:
            print(f"Error creando hilo: {e}")

# Ejecutar el bot
client.run(TOKEN)
