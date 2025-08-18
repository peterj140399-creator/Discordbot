import os
import discord

TOKEN = "TU_TOKEN_DEL_BOT"
WEBHOOK_ID = 1406962453987725392  # ID del webhook "Buzón"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Solo responder a mensajes del webhook
    if message.webhook_id == WEBHOOK_ID:
        thread_name = f"Sugerencia de {message.author.name}"
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
