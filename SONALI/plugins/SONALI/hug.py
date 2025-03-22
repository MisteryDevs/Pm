from SONALI import app
from pyrogram import filters
import nekos

@app.on_message(filters.command("hug"))
async def huggg(client, message):
    try:
        hug_url = nekos.img("hug")  # Nekos se hug ka image URL milega
        
        if not hug_url:  # Agar nekos se valid response nahi mila
            return await message.reply_text("❌ Hug GIF not found!")

        if message.reply_to_message:
            caption = f"🤗 {message.from_user.mention} hugged {message.reply_to_message.from_user.mention}!"
        else:
            caption = "🤗 Sending virtual hugs!"

        # Agar nekos sirf image return karta hai, to reply_photo() use karein
        await message.reply_photo(hug_url, caption=caption)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

__MODULE__ = "Hᴜɢ"
__HELP__ = """
🤗 **Hᴜɢ Cᴏᴍᴍᴀɴᴅ**
- /hug → Sᴇɴᴅ ᴀ ʜᴜɢɢɪɴɢ ɢɪғ/ɪᴍᴀɢᴇ.
- Rᴇᴘʟʏ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ /hug ᴛᴏ ʜᴜɢ ᴛʜᴇᴍ!

✨ **Nᴏᴛᴇ:**  
Bᴏᴛ ᴍᴜsᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ sᴇɴᴅ ɪᴍᴀɢᴇs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.
"""
