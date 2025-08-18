import os
import discord
from dotenv import load_dotenv
import json

# Cargar token del archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# ID del webhook
WEBHOOK_ID = 1406962453987725392  # reemplaza con tu webhook real

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.webhook_id == WEBHOOK_ID:
        thread_name = "Sugerencia de desconocido"  # fallback

        try:
            data = json.loads(message.content)
            # Aquí asumimos que Google Forms envía algo tipo:
            # {"responses":[{"question":"Nombre","answer":"Juan"},{"question":"Edad","answer":"25"}]}
            responses = data.get("responses", [])
            if responses:
                first_answer = responses[0].get("answer", "desconocido")
                thread_name = f"Sugerencia de {first_answer}"
        except json.JSONDecodeError:
            # Si no es JSON, usamos directamente el texto
            thread_name = f"Sugerencia de {message.content[:50]}"

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
