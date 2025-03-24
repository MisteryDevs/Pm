import yt_dlp
import os
from datetime import datetime
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

# Tracking Users Who Used /chkcookies
active_users = set()

# Logs Group ID (Cookies file waha send hogi)
LOGS_GROUP_ID = -1002300353707  

# Stylish Symbols & Fonts for VIP Look
BULLET = "➤"
CHECK = "✅"
CROSS = "❌"
CLOCK = "⏳"
SHIELD = "🛡"
FIRE = "🔥"
STAR = "⭐"
USER = "👤"
TIME = "⏰"

# Step 1: Enable Checking with `/chkcookies`
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users.add(message.chat.id)
    await message.reply(f"{CHECK} ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ ! {CLOCK}")

# Step 2: Accept Only If `/chkcookies` was Used (Only for Documents)
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply(f"{CROSS} ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ `cookies.txt` ғɪʟᴇ!\n✅ Make sure the file is named `cookies.txt`.")
        os.remove(file_path)  # Cleanup
        return

    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply(f"{CROSS} ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ɪs ᴇᴍᴘᴛʏ !")
            os.remove(file_path)  # Cleanup
            return

        # Step 3: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}
        result_msg = ""
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
            result_msg = f"{CHECK} ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ᴠᴀʟɪᴅ ! "
        except yt_dlp.utils.ExtractorError:
            result_msg = f"{CROSS} ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ !"

        await message.reply(result_msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ ᴇʀʀᴏʀ: `{str(e)}`")

    os.remove(file_path)  # Cleanup
    active_users.remove(message.chat.id)  # Remove user

# Step 4: Handle Wrong Inputs But Don't Block Other Commands
@app.on_message(filters.private & ~filters.command(["chkcookies"]) & ~filters.document)
async def warn_wrong_input(client, message):
    if message.chat.id in active_users:
        await message.reply(f"{CROSS} ᴘʟᴇᴀsᴇ sᴇɴᴅ `cookies.txt` ғɪʟᴇ, ɴᴏᴛ ᴛᴇxᴛ ᴏʀ ɪᴍᴀɢᴇ !")
