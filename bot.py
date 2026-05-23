import os
import discord
from discord.ext import commands

# ==== CONFIGURACIÓN DISCORD ====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs de los webhooks
WEBHOOK_IDS = {
    "sugerencia": int(os.environ.get("WEBHOOK_ID")),
    "reporte": int(os.environ.get("WEBHOOK_ID_REPORTE"))
}

# ==== EVENTOS ====
@bot.event
async def on_message(message):

    print("MENSAJE DETECTADO")
    print(f"Webhook ID: {message.webhook_id}")
    print(f"Contenido: {message.content}")

    # Ignorar mensajes del propio bot
    if message.author == bot.user:
        return

    # Detectar mensajes enviados desde webhooks
    if message.webhook_id:

        # WEBHOOK DE SUGERENCIAS
        if message.webhook_id == WEBHOOK_IDS["sugerencia"]:
            try:
                await message.channel.create_thread(
                    name="Sugerencia",
                    message=message
                )
                print("[INFO] Hilo de Sugerencia creado.")
            except Exception as e:
                print(f"[ERROR] No se pudo crear hilo de sugerencia: {e}")

        # WEBHOOK DE REPORTES
        elif message.webhook_id == WEBHOOK_IDS["reporte"]:
            try:
                await message.channel.create_thread(
                    name="Reporte",
                    message=message
                )
                print("[INFO] Hilo de Reporte creado.")
            except Exception as e:
                print(f"[ERROR] No se pudo crear hilo de reporte: {e}")

# ==== EJECUCIÓN ====
bot.run(os.environ.get("DISCORD_TOKEN"))
