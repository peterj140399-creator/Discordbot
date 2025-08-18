import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

WEBHOOK_ID = 1406962453987725392  # reemplaza con tu webhook real

@client.event
async def on_ready():
    print(f'Bot listo. Conectado como: {client.user}')

@client.event
async def on_message(message):
    print(f"Mensaje recibido: author={message.author}, webhook_id={message.webhook_id}, content={message.content}")

    if message.author == client.user:
        print("Ignorando mensaje del bot")
        return

    if message.webhook_id == WEBHOOK_ID:
        # Imprimir contenido del mensaje para depurar
        print(f"Mensaje válido del webhook: {message.content}")

        # Extraer nickname de la primera línea del mensaje
        # Ajusta esto según el formato real de tu Google Form
        try:
            first_line = message.content.split("\n")[0]  # primera línea
            nick = first_line.split(":")[1].strip()      # lo que sigue después de ":"
        except Exception as e:
            print(f"No se pudo extraer nick: {e}")
            nick = "desconocido"

        thread_name = f"Sugerencia de {nick}"
        try:
            await message.channel.create_thread(
                name=thread_name,
                message=message,
                type=discord.ChannelType.public_thread
            )
            print(f"Hilo '{thread_name}' creado correctamente.")
        except Exception as e:
            print(f"Error creando hilo: {e}")

client.run(TOKEN)

