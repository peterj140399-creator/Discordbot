import os
import discord

# Leer token de Render
TOKEN = os.environ.get("DISCORD_TOKEN")

# Intents necesarios para leer mensajes y crear threads
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# ID del webhook del "Buzón"
WEBHOOK_ID = 1406962453987725392  # reemplaza con tu webhook real

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.webhook_id == WEBHOOK_ID:
        try:
            if message.embeds:
                embed = message.embeds[0]
                lines = embed.description.splitlines()
                nick = None
                for i in range(len(lines)-1):
                    question = lines[i].strip()
                    answer = lines[i+1].strip()
                    if question.lower() == "nick en el servidor":
                        nick = answer
                        break

                if not nick:
                    nick = "desconocido"

                thread_name = f"Sugerencia de {nick}"

                await message.channel.create_thread(
                    name=thread_name,
                    message=message,
                    type=discord.ChannelType.public_thread
                )
                print(f"Hilo '{thread_name}' creado.")

        except Exception as e:
            print(f"Error creando hilo: {e}")

client.run(TOKEN)
