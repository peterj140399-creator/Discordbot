import os
import discord
from discord.ext import commands

# Intents mínimos necesarios
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs de los webhooks (poner los valores numéricos en Environment)
WEBHOOK_IDS = {
    "sugerencia": int(os.environ.get("WEBHOOK_ID")),       # webhook sugerencias
    "reporte": int(os.environ.get("WEBHOOK_ID_REPORTE"))  # webhook reportes
}

@bot.event
async def on_ready():
    print(f"[INFO] Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    # Ignorar mensajes propios
    if message.author == bot.user:
        return

    # Comprobar si el mensaje viene de un webhook
    if message.webhook_id:
        if message.webhook_id == WEBHOOK_IDS["sugerencia"]:
            # Crear hilo en el canal de mensaje
            await message.channel.create_thread(
                name="Sugerencia",
                message=message
            )
            print("[INFO] Hilo de Sugerencia creado.")
        
        elif message.webhook_id == WEBHOOK_IDS["reporte"]:
            await message.channel.create_thread(
                name="Reporte",
                message=message
            )
            print("[INFO] Hilo de Reporte creado.")

# Iniciar bot usando token en environment
bot.run(os.environ.get("DISCORD_TOKEN"))
