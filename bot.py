@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.webhook_id == WEBHOOK_ID:
        # Intentar extraer el nick
        nick = "desconocido"
        for line in message.content.split("\n"):
            if line.startswith("Nick en el servidor:"):
                nick = line.replace("Nick en el servidor:", "").strip()
                break

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



