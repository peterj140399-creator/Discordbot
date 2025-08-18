import os
import discord

# Configuración del token y webhook desde Environment
TOKEN = os.environ.get("DISCORD_TOKEN")
WEBHOOK_ID = int(os.environ.get("WEBHOOK_ID"))  # Asegúrate de poner la ID numérica

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

    # Mostrar todos los mensajes recibidos
    print(f"Mensaje recibido: author={message.author}, webhook_id={message.webhook_id}, content={message.content}")

    # Solo responder si el mensaje viene del webhook correcto
    if message.webhook_id == WEBHOOK_ID:
        nick = message.author.name or "desconocido"
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

# Ejecutar el bot
client.run(TOKEN)
