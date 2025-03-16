import random 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from SONALI import app

IMAGE = [
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
    "https://graph.org/file/84e84ff778b045879d24f.jpg",
    "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
    "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
    "https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
    "https://graph.org/file/37248e7bdff70c662a702.jpg",
    "https://graph.org/file/0bfe29d15e918917d1305.jpg",
    "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
    "https://graph.org/file/e6b01f23f2871e128dad8.jpg",
    "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
    "https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
    "https://graph.org/file/39d7277189360d2c85b62.jpg",
    "https://graph.org/file/5846b9214eaf12c3ed100.jpg",
    "https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
    "https://graph.org/file/3514efaabe774e4f181f2.jpg",
]

#--------------------------

MUST_JOIN = "SWEETY_BOT_UPDATE"
#------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    random.choice(IMAGE),
                    caption=f"💖 ʜᴇʏ ᴛʜᴇʀᴇ! ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ.\n\n"
                            f"🚀 **ᴛᴏ ᴜsᴇ 🎵 •⏤‌𝄞⃝🍧 ‌⃪‌𝐒ᴡᴇᴇᴛʏ 𝐌ᴜsɪᴄ♥️꯭꯭꯭꯭ ꯭꯭᪳𝆺𝅥, ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ!\n"
                            f"🔹 **Jᴏɪɴ ᴀɴᴅ ᴜɴʟᴏᴄᴋ ᴀʟʟ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs 💫\n\n"
                            f"🎯 Cʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ:",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔔 ᴜᴘᴅᴀᴛᴇ", url=link),
                                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/APNA_CLUB_09"),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"⚠️ ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ {MUST_JOIN} ғɪʀsᴛ!")
