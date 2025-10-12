import os
import discord
from discord.ext import commands, tasks
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# ==== CONFIGURACIÓN DISCORD ====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs de los webhooks (poner los valores numéricos en Environment)
WEBHOOK_IDS = {
    "sugerencia": int(os.environ.get("WEBHOOK_ID")),        # webhook sugerencias
    "reporte": int(os.environ.get("WEBHOOK_ID_REPORTE"))    # webhook reportes
}

# ==== CONFIGURACIÓN GOOGLE SHEETS ====
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")              # ID del Google Sheet
CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID"))          # Canal donde se publicará el mensaje
SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")  # Contenido del JSON de Google Service Account

# Autenticación con Google Sheets
creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

message_id = None  # Guardará el ID del mensaje que el bot actualizará

# ==== FUNCIONES AUXILIARES ====
def obtener_datos():
    """Obtiene los datos del Google Sheet y los formatea para Discord."""
    data = sheet.get_all_records()
    if not data:
        return "No hay datos aún en la hoja."
    
    # Ordenar de mayor a menor participaciones
    data.sort(key=lambda x: int(x.get("Participaciones", 0)), reverse=True)

    texto = "# :jack_o_lantern: Recuento de participaciones del sorteo :jack_o_lantern:\n\n"
    for fila in data:
        nick = fila.get("Nick", "Desconocido")
        participaciones = fila.get("Participaciones", 0)
        texto += f"**{nick}** — {participaciones} :jack_o_lantern:\n"
    
    return texto

# ==== EVENTOS DEL BOT ====
@bot.event
async def on_ready():
    print(f"[INFO] Bot conectado como {bot.user}")
    actualizar_mensaje.start()  # Inicia la tarea automática

@bot.event
async def on_message(message):
    # Ignorar mensajes propios
    if message.author == bot.user:
        return

    # Comprobar si el mensaje viene de un webhook
    if message.webhook_id:
        if message.webhook_id == WEBHOOK_IDS["sugerencia"]:
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

# ==== TAREA AUTOMÁTICA ====
@tasks.loop(seconds=10)
async def actualizar_mensaje():
    """Actualiza el mensaje del sorteo cada 300 segundos."""
    global message_id
    canal = bot.get_channel(CHANNEL_ID)
    if canal is None:
        print("❌ No se pudo acceder al canal.")
        return

    texto = obtener_datos()

    if message_id is None:
        msg = await canal.send(texto)
        message_id = msg.id
        print(f"📝 Mensaje creado con ID {message_id}")
    else:
        try:
            msg = await canal.fetch_message(message_id)
            await msg.edit(content=texto)
            print("♻️ Mensaje actualizado correctamente")
        except discord.NotFound:
            msg = await canal.send(texto)
            message_id = msg.id
            print("🔁 Mensaje recreado porque fue eliminado")

# ==== EJECUCIÓN ====
bot.run(os.environ.get("DISCORD_TOKEN"))











