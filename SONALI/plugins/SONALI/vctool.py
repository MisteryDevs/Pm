from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI import app
from config import OWNER_ID
import aiohttp
import re

# ✅ VC On
@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    await msg.reply("😍 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ 🥳")

# ✅ VC Off
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
    await msg.reply("😕 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ 💔")

# ✅ Invite Members on VC (Fixed)
@app.on_message(filters.video_chat_members_invited)
async def brah3(_, message: Message):
    if message.video_chat_members_invited:
        invited_users = message.video_chat_members_invited.users
        invited_text = f"{message.from_user.mention} 👈 ɪɴᴠɪᴛᴇᴅ 👉 "

        for user in invited_users:
            try:
                invited_text += f"<a href='tg://user?id={user.id}'>{user.first_name}</a> "
            except Exception:
                continue
        
        await message.reply(invited_text, parse_mode="HTML")  # Fixed parse_mode

# ✅ Math Calculation Command
@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):   
    try:
        expression = message.text.split("/math ", 1)[1]
        result = eval(expression)
        response = f"ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs : {result}"
    except:
        response = "ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ"
    
    message.reply(response)

# ✅ Leave Group Command
@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    text = "sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ !!."
    await message.reply_text(text)
    await app.leave_chat(chat_id=chat_id, delete=True)

# ✅ Google Search Command (Fixed)
@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(_, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a search query!")
    
    query = message.text.split(maxsplit=1)[1]
    msg = await message.reply("Searching...")

    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(f"https://content-customsearch.googleapis.com/customsearch/v1",
                               params={"cx": "ec8db9e1f9e41e65e", "q": query, 
                                       "key": "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM", 
                                       "start": start},
                               headers={"x-referer": "https://explorer.apis.google.com"}) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")

            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                link = re.sub(r'\/\d', "", link.split("?")[0])  # Remove /s and ? params
                if link in result:
                    continue  # Remove duplicates
                result += f"{title}\n{link}\n\n"

            await msg.edit(result, link_preview=False)
