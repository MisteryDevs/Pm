from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

# 🎭 Command to get sticker ID
@app.on_message(filters.command("strikerid") & filters.reply)
async def get_sticker_id(client, message: Message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker_id = message.reply_to_message.sticker.file_id
        await message.reply_text(f"🆔 sᴛɪᴄᴋᴇʀ ɪᴅ :\n`{sticker_id}`")
    else:
        await message.reply_text("⚠️Rᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ to ɢᴇᴛ ɪᴛs ɪᴅ.")

# 🎭 Command to send sticker using ID
@app.on_message(filters.command("getstriker"))
async def send_sticker(client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("⚠️ ᴜsᴀɢᴇ: `/getstriker <sticker_id>`")
    
    sticker_id = args[1]
    try:
        await client.send_sticker(
            chat_id=message.chat.id,
            sticker=sticker_id
        )
    except Exception as e:
        await message.reply_text(f"❌ Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴛɪᴄᴋᴇʀ.\n\n`{e}`")
