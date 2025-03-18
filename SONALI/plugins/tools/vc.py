from pyrogram import filters
from pyrogram.types import Message
from tgvc import VcPlayer

from SONALI import app  # Jo bhi tera main bot ka client instance hai
vc_player = VcPlayer(app)

# ✅ Voice Chat Start Event
@app.on_message(filters.voice_chat_started)
async def vc_started(client, message):
    user = message.from_user.mention
    await message.reply_text(f"🎙️ Voice Chat Started by {user}!")

# 🔴 Voice Chat End Event
@app.on_message(filters.voice_chat_ended)
async def vc_ended(client, message):
    await message.reply_text("🔴 Voice Chat has Ended!")

# 🎵 Play Command with Admin Check
@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message: Message):
    chat_id = message.chat.id
    bot_member = await client.get_chat_member(chat_id, "me")

    if not bot_member.privileges.can_manage_voice_chats:
        await message.reply_text("🚫 Bot is not an admin in VC! Please give admin rights.")
        return

    # Agar bot admin hai, toh yeh existing `/play` ka system trigger karega
    await vc_player.play(message)
