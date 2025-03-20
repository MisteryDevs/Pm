import asyncio
from SONALI import app  # ✅ Importing your bot module
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

@app.on_message(filters.command(["genstring", "string", "session"]) & filters.private)
async def start_message(client, message):
    user_name = message.from_user.first_name  
    photo_url = "https://i.ibb.co/39WSm9zM/IMG-20250207-080405-192.jpg"

    # ✅ Simulate loading progress  
    loading_message = await message.reply_text("[□□□□□□□□□□] 0%")

    progress = [
        "[■□□□□□□□□□] 10%", "[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", "[■■■■□□□□□□] 40%",
        "[■■■■■□□□□□] 50%", "[■■■■■■□□□□] 60%", "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 80%",
        "[■■■■■■■■■□] 90%", "[■■■■■■■■■■] 100%"
    ]

    for step in progress:
        await loading_message.edit_text(f"{step}")
        await asyncio.sleep(0.3)

    await loading_message.edit_text("❖ Jᴀʏ Sʜʀᴇᴇ Rᴀᴍ 🚩...")
    await asyncio.sleep(1)
    await loading_message.delete()

    # 🎭 INLINE BUTTONS 🎭  
    buttons = [
        [
            InlineKeyboardButton(" ᴘʏꝛσɢꝛᴧϻ", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#pyrogram,user")),
            InlineKeyboardButton(" ᴛᴇʟᴇᴛʜᴏɴ", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#telethon,user")),
            InlineKeyboardButton(" ɢꝛᴧϻ ᴊs", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#gramjs,user"))
        ],
        [
            InlineKeyboardButton(" ᴏᴡɴᴇʀ", url="https://t.me/PRINCE_WEBZ"),
            InlineKeyboardButton(" ᴜᴘᴅᴀᴛᴇ", url="https://t.me/SWEETY_BOT_UPDATE")
        ],
        [
            InlineKeyboardButton("🔙 ˹ ʙᴧᴄᴋ ˼", callback_data="settings_back_helper")
        ]
    ]

    # 🎭 STYLISH CAPTION 
    caption_text = f"""
╭─────────◆◇◆─────────╮
  🎭 𝙷𝙴𝚈 !! {user_name}
╰─────────◆◇◆─────────╯
╭━━━〔 ɪɴғᴏʀᴍᴀᴛɪᴏɴ 〕━━━╮
┣  ɪ'ᴍ ᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ ! 
┣ ᴜsᴇ ᴍᴇ ᴛᴏ ɢᴀɴᴇʀᴀᴛᴇ sᴇssɪᴏɴs
┣  sᴜᴘᴘᴏʀᴛ : ᴘʏʀᴏɢʀᴀᴍ | ᴛᴇʟᴇᴛʜᴏɴ | ɢʀᴀᴍᴊꜱ  
┣  ɴᴏ ɪᴅ ʟᴏɢᴏᴜᴛ ɪssᴜᴇ ! 
╰━━━━━━━━━━━━━━━━━━╯  

𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲 : @PRINCE_WEBZ
"""

    await message.reply_photo(
        photo=photo_url,
        caption=caption_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
