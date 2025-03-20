from SONALI import app  # ✅ SONALI bot import
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ /genstring, /string, /session Commands
@app.on_message(filters.command(["genstring", "string", "session"]) & filters.private)
async def generate_session(_, message):
    photo_url = "https://i.ibb.co/39WSm9zM/IMG-20250207-080405-192.jpg"

    # Inline buttons
    buttons = [
        [InlineKeyboardButton("⚡ Pyrogram", url="https://telegram.tools/session-string-generator#pyrogram")],
        [InlineKeyboardButton("🔥 Telethon", url="https://telegram.tools/session-string-generator#telethon")],
        [InlineKeyboardButton("🚀 GramJS", url="https://telegram.tools/session-string-generator#gramjs")]
    ]
    
    await message.reply_photo(
        photo=photo_url,
        caption="**⚡ Generate Your Telegram Session String:**\n\n👇 Select Your Preferred Library Below 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
  )
