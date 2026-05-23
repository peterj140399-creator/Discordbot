import os
import discord
from discord.ext import commands

# ==== CONFIGURACIÓN DISCORD ====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==== WEBHOOK IDS ====
WEBHOOK_IDS = {
    "sugerencia": int(os.environ.get("WEBHOOK_ID")),
    "reporte": int(os.environ.get("WEBHOOK_ID_REPORTE"))
}

# ==== READY ====
@bot.event
async def on_ready():
    print(f"[INFO] Bot conectado como {bot.user}")

# ==== DETECCIÓN WEBHOOKS ====
@bot.event
async def on_message(message):

    # ignorar el propio bot
    if message.author == bot.user:
        return

    # SOLO mensajes de webhook
    if message.webhook_id:

        print(f"[DEBUG] Webhook recibido: {message.webhook_id}")

        # SUGERENCIAS
        if message.webhook_id == WEBHOOK_IDS["sugerencia"]:
            try:
                await message.channel.create_thread(
                    name="Sugerencia",
                    message=message
                )
                print("[INFO] Hilo de Sugerencia creado.")
            except Exception as e:
                print(f"[ERROR] Sugerencia: {e}")

        # REPORTES
        elif message.webhook_id == WEBHOOK_IDS["reporte"]:
            try:
                await message.channel.create_thread(
                    name="Reporte",
                    message=message
                )
                print("[INFO] Hilo de Reporte creado.")
            except Exception as e:
                print(f"[ERROR] Reporte: {e}")

# ==== RUN ====
bot.run(os.environ.get("DISCORD_TOKEN"))
