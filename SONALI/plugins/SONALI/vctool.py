from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI import app
from config import OWNER_ID
import aiohttp
import re

# ✅ VC Started (Auto-detect)
@app.on_message(filters.video_chat_started)
async def vc_started(_, msg):
    await msg.reply("😍 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ 🥳")

# ❌ VC Ended (Auto-detect)
@app.on_message(filters.video_chat_ended)
async def vc_ended(_, msg):
    await msg.reply("😕 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ 💔")

# 🎟 Invite Members to VC
@app.on_message(filters.video_chat_members_invited)
async def vc_invite(client, message: Message):
    text = f"{message.from_user.mention} 👈ɪɴᴠɪᴛᴇᴅ👉 "
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
        except Exception:
            pass
    try:
        await message.reply(f"{text} 🤭🤭")
    except:
        pass

# 🎤 Start Voice Chat Manually
@app.on_message(filters.command(["stvc", "startvc", "vcstart"]) & filters.user(OWNER_ID))
async def start_vc(client, message):
    chat_id = message.chat.id
    try:
        await client.invoke(
            "StartScheduledVoiceChat",
            peer=chat_id
        )
        await message.reply("🎙️ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʜᴀs ʙᴇᴇɴ sᴛᴀʀᴛᴇᴅ ✅")
    except Exception as e:
        await message.reply(f"⚠️ ғᴀɪʟᴇᴅ ᴛᴏ sᴛᴀʀᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ:\n`{e}`")

# 🚪 End Voice Chat Manually
@app.on_message(filters.command(["end", "endvc", "vcend"]) & filters.user(OWNER_ID))
async def end_vc(client, message):
    chat_id = message.chat.id
    try:
        await client.invoke(
            "DiscardGroupCall",
            peer=chat_id
        )
        await message.reply("❌ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʜᴀs ʙᴇᴇɴ ᴇɴᴅᴇᴅ 💔")
    except Exception as e:
        await message.reply(f"⚠️ ғᴀɪʟᴇᴅ ᴛᴏ ᴇɴᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ:\n`{e}`")

# 🧮 Math Command
@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):   
    expression = message.text.split("/math ", 1)[1]
    try:        
        result = eval(expression)
        response = f"📊 ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs: `{result}`"
    except:
        response = "⚠️ ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ!"
    message.reply(response)

# 📤 Bot Leave Group Command
@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def bot_leave(client, message):
    chat_id = message.chat.id
    text = "🤖 sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴛʜɪs ᴄʜᴀᴛ! 🚀"
    await message.reply_text(text)
    await client.leave_chat(chat_id=chat_id, delete=True)

# 🔍 Google Search Command
@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}", headers={"x-referer": "https://explorer.apis.google.com"}) as r:
            response = await r.json()
            result = ""
            
            if not response.get("items"):
                return await msg.edit("No results found!")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r'\/\d', item["link"]):
                    link = re.sub(r'\/\d', "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    continue
                result += f"{title}\n{link}\n\n"
            await msg.edit(result, link_preview=False)
            await session.close()
