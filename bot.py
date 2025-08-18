import os
import discord

# Token y webhook ID desde las variables de entorno de Render
TOKEN = os.environ.get("DISCORD_TOKEN")
WEBHOOK_ID = int(os.environ.get("WEBHOOK_ID"))  # Asegúrate de poner la ID numérica

# Intents necesarios para leer mensajes y crear threads
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo responder si el mensaje viene del webhook
    if message.webhook_id == WEBHOOK_ID:
        print(f"\nMensaje recibido del webhook: '{message.content}'")
        print(f"Autor webhook: {message.author} - Nick detectado: '{message.author.name}'")
        thread_name = f"Sugerencia de {message.author.name}"
        print(f"Intentando crear hilo con nombre: '{thread_name}'")
        try:
            await message.channel.create_thread(
                name=thread_name,
                message=message,
                type=discord.ChannelType.public_thread  # público en el canal
            )
            print(f"Hilo '{thread_name}' creado con éxito.")
        except Exception as e:
            print(f"Error creando hilo: {e}")

client.run(TOKEN)
