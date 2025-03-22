from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command("strikerid") & filters.reply)
async def get_sticker_id(client, message: Message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker_id = message.reply_to_message.sticker.file_id
        await message.reply_text(f"🆔 sᴛɪᴄᴋᴇʀ ɪᴅ:\n`{sticker_id}`")
    else:
        await message.reply_text("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢʀᴇᴀᴛ ɪᴛ ɢᴇᴛ ɪᴛs ɪᴅ")
