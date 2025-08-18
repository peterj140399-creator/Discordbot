import os
import discord

# Token desde variable de entorno
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# ID de tu webhook
WEBHOOK_ID = 1406962453987725392  # reemplaza con tu webhook real

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo responder si el mensaje viene del webhook específico
    if message.webhook_id == WEBHOOK_ID:
        # Extraer nick de la primera línea del embed si existe
        nick = "desconocido"
        if message.embeds:
            embed = message.embeds[0]
            if embed.description:
                # Tomamos la primera línea de la descripción
                lineas = embed.description.splitlines()
                if lineas:
                    nick = lineas[0].strip()

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
