import yt_dlp
import os
from SONALI import app
from pyrogram import filters

# Step 1: User Sends `cookies.txt`
@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message):
    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply("❌ **Please send a valid** `cookies.txt` **file!**")
        return

    # Step 2: Read Cookies File
    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply("❌ **Your cookies.txt file is empty!**")
            os.remove(file_path)  # Delete temp file
            return

        # Step 3: Validate YouTube Cookies
        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            await message.reply("✅ **Your YouTube cookies are valid!** 🎉", quote=True)
        except yt_dlp.utils.ExtractorError:
            await message.reply("❌ **Your YouTube cookies are invalid or expired!**", quote=True)

    except Exception as e:
        await message.reply(f"⚠️ **Error reading file:** `{str(e)}`")

    # Step 4: Clean Up Temporary File
    os.remove(file_path)
