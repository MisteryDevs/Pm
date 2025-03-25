from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI import app
from config import OWNER_ID

# ✅ Voice Chat Started
@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    await msg.reply("😍 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ 🥳")

# ✅ Voice Chat Ended
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
    await msg.reply("😕 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ 💔")

# ✅ Invite Members on VC (Fixed HTML Mention)
@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    text = f"{message.from_user.mention} 👈ɪɴᴠɪᴛᴇᴅ ᴛᴏ👉 "
    invited_users = []

    for user in message.video_chat_members_invited.users:
        try:
            invited_users.append(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>")
        except Exception:
            pass

    if invited_users:
        text += ", ".join(invited_users) + " 🤭🤭"
        await message.reply(text, parse_mode="HTML")


# ✅ Math Expression Calculator
@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):   
    expression = message.text.split("/math ", 1)[1]
    try:        
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


# ✅ Google Search Functionality
import aiohttp
import re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.reply("🔎 Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?"
            f"cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&"
            f"key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"}
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")

            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                
                # Clean the link
                link = re.sub(r'\/\d', "", link) if re.search(r'\/\d', link) else link
                link = link.split("?")[0] if "?" in link else link
                
                if link in result:
                    continue  # Avoid duplicates

                result += f"<b>{title}</b>\n<a href='{link}'>{link}</a>\n\n"

            next_btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("▶️ Next ▶️", callback_data=f"next {start+10} {event.text.split()[1]}")]
            ])
            await msg.edit(result, parse_mode="HTML", disable_web_page_preview=True, reply_markup=next_btn)
