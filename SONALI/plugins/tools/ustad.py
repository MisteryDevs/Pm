from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from SONALI import app  # Ensure this is correctly imported

@app.on_message(filters.command("owner"))
async def owner_info(client: Client, message: Message):
    # Group ke liye alag image, private chat ke liye alag image
    photo_url = "https://i.ibb.co/39WSm9zM/IMG-20250207-080405-192.jpg" if message.chat.type == "private" else "https://i.ibb.co/39WSm9zM/IMG-20250207-080405-192.jpg"

    # Owner link (jitna bhi required ho, ek hi button me rakh diya hai)
    owner_url = "https://t.me/PRINCE_WEBZ"

    await message.reply_photo(
        photo=photo_url,
        caption="🥀 𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞 𝐅𝐨𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫 🥀",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🗡️ 𝐎ᴡɴᴇʀ 🗡️", url=owner_url)]
            ]
        ),
    )
