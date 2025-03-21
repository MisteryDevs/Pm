import re
import asyncio
from SONALI import app  # Tumhare bot ka instance
from pyrogram import filters
from pyrogram.types import Message

# MongoDB Message
MONGO_MESSAGE = """❤ 𝐇𝐄𝐑𝐄 𝐒𝐎𝐌𝐄 𝐌𝐎𝐍𝐆𝐎 𝐃𝐁 ❤

• ɪғ ᴀɴʏ ᴍᴏɴɢᴏ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ, ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ᴏɴᴇ:

"mongodb+srv://hnyx:wywyw2@cluster0.9dxlslv.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://ravi:ravi12345@cluster0.hndinhj.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://userbot:userbot@cluster0.iweqz.mongodb.net/test?retryWrites=true&w=majority"

"mongodb+srv://Alisha:Alisha123@cluster0.yqcpftw.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://vikashgup87:EDRIe3bdEq85Pdpl@cluster0.pvoygcu.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://Sarkar123:GAUTAMMISHRA@sarkar.1uiwqkd.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://kuldiprathod2003:kuldiprathod2003@cluster0.wxqpikp.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority"
"mongodb+srv://rahul:rahulkr@cluster0.szdpcp6.mongodb.net/?retryWrites=true&w=majority"

"mongodb+srv://knight_rider:GODGURU12345@knight.jm59gu9.mongodb.net/?retryWrites=true&w=majority"

❀ ᴜsᴇ ᴋʀᴏ ᴀɴᴅ ᴇɴᴊᴏʏ ᴋʀᴏ ᴡᴏʀᴋɪɴɢ ʜᴀɪ ʏᴀ ɴʜɪ ᴄʜᴇᴄᴋ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ ``/chkmongo ᴍᴏɴɢᴏ ᴜʀʟ ᴅᴀʟᴏ ❀
"""

@app.on_message(filters.command(["mongo", "mongodb"]) & filters.private)
async def send_mongo_details(client, message: Message):
    # Agar sirf "/mongo" ya "/mongodb" likha hai tabhi reply kare, warna ignore kare
    if len(message.command) == 1:
        await message.reply_text(MONGO_MESSAGE)
