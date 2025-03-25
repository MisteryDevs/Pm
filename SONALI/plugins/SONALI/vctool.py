import aiohttp
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SONALI import app
from config import OWNER_ID

OWNER_USERNAME = "@PRINCE_WEBZ"  

@app.on_message(filters.video_chat_started)
async def vc_on(_, msg):
    await msg.reply("😍ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ🥳")

@app.on_message(filters.video_chat_ended)
async def vc_off(_, msg):
    await msg.reply("😕ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ💔")

# ✅ Math Calculation Command
@app.on_message(filters.command("math", prefixes="/"))
async def calculate_math(_, message):
    try:
        expression = message.text.split("/math ", 1)[1]
        result = eval(expression)
        response = f"🧮 Result: `{result}`"
    except:
        response = "⚠️ Invalid Expression!"
    
    await message.reply(response)

# ✅ Leave Group Command (Only for Owner)
@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    await message.reply_text("✅ Successfully Left The Group")
    await app.leave_chat(chat_id=chat_id, delete=True)

# ✅ Google Search Command with Clean Output
@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(_, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Provide a search query!")
    
    query = message.text.split(maxsplit=1)[1]
    msg = await message.reply("🔍 Searching...")

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://content-customsearch.googleapis.com/customsearch/v1",
            params={
                "cx": "ec8db9e1f9e41e65e",
                "q": query,
                "key": "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM",
            },
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("⚠️ No Results Found!")

            for item in response["items"]:
                title = item["title"]
                link = re.sub(r"\/\d", "", item["link"].split("?")[0])  # Clean URL
                result += f"🔹 {title}\n🔗 [Click Here]({link})\n\n"

            btn = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔍 Search Again", switch_inline_query_current_chat="")]]
            )

            await msg.edit(result, disable_web_page_preview=True, reply_markup=btn)
