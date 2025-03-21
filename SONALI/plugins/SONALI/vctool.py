from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI import app
from config import OWNER_ID
import aiohttp
import re

# ✅ VC Started
@app.on_message(filters.video_chat_started)
async def vc_started(_, msg):
    await msg.reply("😍 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ 🥳")

# ❌ VC Ended
@app.on_message(filters.video_chat_ended)
async def vc_ended(_, msg):
    await msg.reply("😕 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ 💔")

# 🎤 VC Join Message
@app.on_message(filters.video_chat_participant_added)
async def vc_join(client, message: Message):
    for user in message.video_chat_participants_added:
        try:
            await message.reply(f"✅ {user.mention} ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ! 🎤")
        except:
            pass

# 🚪 VC Leave Message
@app.on_message(filters.video_chat_participant_removed)
async def vc_leave(client, message: Message):
    for user in message.video_chat_participants_removed:
        try:
            await message.reply(f"❌ {user.mention} ʟᴇғᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ! 😔")
        except:
            pass

# 🎟 Invite Members to VC
@app.on_message(filters.video_chat_members_invited)
async def vc_invite(client, message: Message):
    text = f"🔊 {message.from_user.mention} ɪɴᴠɪᴛᴇᴅ: "
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
        except Exception:
            pass
    try:
        await message.reply(f"{text} 🎧")
    except:
        pass

# 🧮 Math Command
@app.on_message(filters.command("math", prefixes="/"))
async def calculate_math(client, message):
    try:
        expression = message.text.split("/math ", 1)[1]
        result = eval(expression)
        response = f"📊 ʀᴇsᴜʟᴛ: `{result}`"
    except:
        response = "⚠️ ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ!"
    await message.reply(response)

# 📤 Bot Leave Group Command
@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def bot_leave(client, message):
    chat_id = message.chat.id
    text = "🤖 ʟᴇᴀᴠɪɴɢ ᴛʜɪs ᴄʜᴀᴛ... 🚀"
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
                    # remove duplicates
                    continue
                result += f"{title}\n{link}\n\n"
            await msg.edit(result, link_preview=False)
            await session.close()
