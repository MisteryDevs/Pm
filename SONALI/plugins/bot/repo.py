from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI import app
from config import BOT_USERNAME

start_txt = """
❖ ʜᴇʏ , ᴛʜᴇʀᴇ ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ  ♥︎\n\n● ɪғ ʏᴏᴜ ᴡᴀɴᴛ "•⏤‌𝄞⃝🍧 ‌⃪‌𝐒ᴡᴇᴇᴛʏ 𝐌ᴜsɪᴄ♥️꯭꯭꯭꯭ ꯭꯭᪳𝆺゙゙𝅥, ʙᴏᴛ ʀᴇᴘᴏ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴄᴏʟʟᴇᴄᴛ ᴍʏ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ.\n\n❖ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ •⏤‌𝄞⃝🍧 ‌⃪‌𝐒ᴡᴇᴇᴛʏ 𝐌ᴜsɪᴄ♥️꯭꯭꯭꯭ ꯭꯭᪳𝆺𝅥 """




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [
          InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/SWEETY_BOT_UPDATE"),
          InlineKeyboardButton("ʀᴇᴘᴏ", url="https://princesinff.serv00.net/")
          ],
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://i.ibb.co/xSQPypBt/IMG-20250315-235146-523.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
  
