import os
import discord
from discord import Webhook, RequestsWebhookAdapter

intents = discord.Intents.default()
intents.messages = True

TOKEN = os.environ.get("DISCORD_TOKEN")
WEBHOOK_ID = int(os.environ.get("WEBHOOK_ID"))
WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN")
GUILD_ID = int(os.environ.get("GUILD_ID"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignorar mensajes del bot mismo
    if message.author == client.user:
        return

    # Solo reaccionar a mensajes del webhook específico
    if message.webhook_id != WEBHOOK_ID:
        return

    # Determinar el tipo de hilo según el título del embed
    thread_name = "Sugerencia"  # valor por defecto
    if message.embeds:
        embed_title = message.embeds[0].title.lower()
        if "reporte" in embed_title:
            thread_name = "Reporte"
        elif "sugerencia" in embed_title:
            thread_name = "Sugerencia"

    # Crear hilo en el canal donde se envió el mensaje
    if message.channel.type == discord.ChannelType.text:
        thread = await message.channel.create_thread(
            name=thread_name,
            message=message
        )
        print(f"Hilo '{thread_name}' creado.")

client.run(TOKEN)
