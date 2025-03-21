import re
import asyncio
from SONALI import app  # Tumhare bot ka instance
from pyrogram import filters
from pyrogram.types import Message

# MongoDB Message
MONGO_MESSAGE = """❤ 𝐇𝐄𝐑𝐄 𝐒𝐎𝐌𝐄 𝐌𝐎𝐍𝐆𝐎 𝐃𝐁 ❤

• ɪғ ᴀɴʏ ᴍᴏɴɢᴏ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ, ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ᴏɴᴇ:

```mongodb+srv://hnyx:wywyw2@cluster0.9dxlslv.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://ravi:ravi12345@cluster0.hndinhj.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://userbot:userbot@cluster0.iweqz.mongodb.net/test?retryWrites=true&w=majority```
```mongodb+srv://Alisha:Alisha123@cluster0.yqcpftw.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://vikashgup87:EDRIe3bdEq85Pdpl@cluster0.pvoygcu.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://Sarkar123:GAUTAMMISHRA@sarkar.1uiwqkd.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://kuldiprathod2003:kuldiprathod2003@cluster0.wxqpikp.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://Alisha:Alisha123@cluster0.yqcpftw.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://rahul:rahulkr@cluster0.szdpcp6.mongodb.net/?retryWrites=true&w=majority```
```mongodb+srv://knight_rider:GODGURU12345@knight.jm59gu9.mongodb.net/?retryWrites=true&w=majority```

❀ ᴜsᴇ ᴋʀᴏ ᴀɴᴅ ᴇɴᴊᴏʏ ᴋʀᴏ ᴡᴏʀᴋɪɴɢ ʜᴀɪ ʏᴀ ɴʜɪ ᴄʜᴇᴄᴋ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ ``/chkmongo ᴍᴏɴɢᴏ ᴜʀʟ ᴅᴀʟᴏ ❀
"""

# Regex for MongoDB URLs
mongo_url_pattern = re.compile(r"mongodb\+srv://[^\s]+")

# ✅ Agar koi `/mongo` ya `/mongodb` likhe to pura list bheje
@app.on_message(filters.command(["mongo", "mongodb"]) & (filters.private | filters.group | filters.channel))
async def send_mongo_links(client, message: Message):
    try:
        await asyncio.sleep(1)  # Floodwait handling
        await message.reply(MONGO_MESSAGE)
    except Exception as e:
        print(f"Error sending Mongo message: {e}")

# ✅ Agar kisi message me MongoDB URL ho aur koi uspe tag kare ya reply kare to auto-copy ho
@app.on_message(filters.text & (filters.private | filters.group | filters.channel))
async def auto_copy_mongo_url(client, message: Message):
    try:
        # Check agar reply wale message me MongoDB URL hai
        if message.reply_to_message and message.reply_to_message.text:
            mongo_links = mongo_url_pattern.findall(message.reply_to_message.text)
            if mongo_links:
                copied_links = "\n".join(f"```{link}```" for link in mongo_links)
                await asyncio.sleep(1)
                await message.reply(f"✅ **Copied MongoDB URL:**\n{copied_links}")
                return

        # Check agar message ke andar koi MongoDB URL mention kiya gaya hai
        mongo_links = mongo_url_pattern.findall(message.text)
        if mongo_links:
            copied_links = "\n".join(f"```{link}```" for link in mongo_links)
            await asyncio.sleep(1)
            await message.reply(f"✅ **Copied MongoDB URL:**\n{copied_links}")

    except Exception as e:
        print(f"Error copying Mongo URL: {e}")
