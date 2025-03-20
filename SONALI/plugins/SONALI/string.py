from SONALI import app  # ✅ Importing your bot module
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

@app.on_message(filters.command(["genstring", "string", "session"]) & filters.private)
async def generate_session(_, message):
    user_name = message.from_user.first_name  # ✅ Fetching User's Name  
    photo_url = "https://i.ibb.co/39WSm9zM/IMG-20250207-080405-192.jpg"

    # ⚡ PREMIUM INLINE BUTTONS ⚡  
    buttons = [
        [
            InlineKeyboardButton(" Pyrogram", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#pyrogram")),
            InlineKeyboardButton("Telethon", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#telethon")),
            InlineKeyboardButton(" GramJS", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#gramjs"))
        ],
        [
            InlineKeyboardButton("💎 String Session", web_app=WebAppInfo(url="https://telegram.tools/session-string-generator")),
        ],
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/PRINCE_WEBZ"),
            InlineKeyboardButton(" ᴜᴘᴅᴀᴛᴇ ", url="https://t.me/SWEETY_BOT_UPDATE")
        ]
    ]
    
    # 🎭 STYLISH CAPTION 🎭  
    caption_text = f"""
╭─────────◆◇◆─────────╮
  🎭 **𝙷𝙴𝚈 !! {user_name}**
╰─────────◆◇◆─────────╯
╭━━━〔 🔹 **𝙸𝙽𝙵𝙾𝚁𝙼𝙰𝚃𝙸𝙾𝙽** 🔹〕━━━╮
┣ 𝙸'𝚖 𝙰 𝚂𝚝𝚛𝚒𝚗𝚐 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚘𝚛 𝙱𝚘𝚝! 
┣ 𝚄𝚜𝚎 𝙼𝚎 𝚃𝚘 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚎 𝚂𝚎𝚜𝚜𝚒𝚘𝚗𝚜.
┣ 𝚞𝚙𝚙𝚘𝚛𝚝: ᴘʏʀᴏɢʀᴀᴍ | ᴛᴇʟᴇᴛʜᴏɴ | ɢʀᴀᴍᴊꜱ  
┣ 𝙽𝚘 𝙸𝙳 𝙻𝚘𝚐𝚘𝚞𝚝 𝙸𝚜𝚜𝚞𝚎!
╰━━━━━━━━━━━━━━━━━━━╯  

𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲 : [•⏤‌𝄞⃝🍧 ‌⃪‌𝐒ᴡᴇᴇᴛʏ 𝐌ᴜsɪᴄ♥️꯭꯭꯭꯭ ꯭꯭᪳𝆺𝅥](https://t.me/SWEETY_BOT_UPDATE) ❤️‍🔥
"""

    await message.reply_photo(
        photo=photo_url,
        caption=caption_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
