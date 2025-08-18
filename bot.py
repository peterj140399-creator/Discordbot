import os
import discord

intents = discord.Intents.default()
intents.messages = True

TOKEN = os.environ.get("DISCORD_TOKEN")
WEBHOOK_ID = int(os.environ.get("WEBHOOK_ID"))

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo reaccionar a mensajes del webhook específico
    if message.webhook_id != WEBHOOK_ID:
        return

    # Crear hilo siempre llamado "Sugerencia"
    if message.channel.type == discord.ChannelType.text:
        await message.channel.create_thread(
            name="Sugerencia",
            message=message
        )
        print("Hilo 'Sugerencia' creado.")

client.run(TOKEN)
