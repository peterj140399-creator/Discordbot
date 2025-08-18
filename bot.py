import os
import discord

# Cargar token y webhook ID desde environment variables
TOKEN = os.environ.get("DISCORD_TOKEN")
WEBHOOK_ID = int(os.environ.get("WEBHOOK_ID"))  # Asegúrate de poner la ID numérica en Environment

# Intents necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[INFO] Bot conectado como {client.user}")

@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Solo responder a mensajes del webhook correcto
    if message.webhook_id == WEBHOOK_ID:
        lines = message.content.splitlines()
        nick = "desconocido"

        # Buscar la línea que sigue a "Nick en el servidor"
        for i, line in enumerate(lines):
            if line.strip().lower() == "nick en el servidor" and i + 1 < len(lines):
                nick = lines[i + 1].strip()
                break

        thread_name = f"Sugerencia de {nick}"
        try:
            await message.channel.create_thread(
                name=thread_name,
                message=message,
                type=discord.ChannelType.public_thread
            )
            print(f"[INFO] Hilo '{thread_name}' creado.")
        except Exception as e:
            print(f"[ERROR] Error creando hilo: {e}")

client.run(TOKEN)
