from SONALI import app
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter  # ✅ सही Import

import asyncio

# टैगिंग स्टेटस ट्रैक करने के लिए
tagging_enabled = {}

# ✅ @all या #all कमांड हैंडलर
@app.on_message(filters.command(["all", "#all"], prefixes=["@", "#"]) & filters.group)
async def tag_all(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ✅ चेक करें कि यूजर एडमिन है या नहीं (Fixed)
    admins = [admin.user.id async for admin in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]
    if user_id not in admins:
        return await message.reply_text("🚫 **सिर्फ एडमिन ही @all कमांड चला सकते हैं!**")

    tagging_enabled[chat_id] = True  # टैगिंग को ऑन करें

    # ✅ ग्रुप के सभी यूज़र्स को लिस्ट करें
    members = [member.user async for member in client.get_chat_members(chat_id)]
    tagged_users = []

    # ✅ एक बार में 5-5 यूजर्स को टैग करें
    for i in range(0, len(members), 5):
        if not tagging_enabled.get(chat_id, False):
            break

        group = members[i:i+5]
        text = "🔥 **Attention Everyone!** 🔥\n\n" + " ".join([f"[{user.first_name}](tg://user?id={user.id})" for user in group])
        
        tagged_users.append(text)
        await message.reply_text(text, disable_web_page_preview=True)
        await asyncio.sleep(2)  # थोड़ा डिले रखें स्पैम से बचने के लिए

    tagging_enabled[chat_id] = False  # टैगिंग को बंद करें

# ✅ /cancel कमांड हैंडलर
@app.on_message(filters.command("cancel") & filters.group)
async def cancel_tagging(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ✅ चेक करें कि यूजर एडमिन है या नहीं (Fixed)
    admins = [admin.user.id async for admin in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]
    if user_id not in admins:
        return await message.reply_text("🚫 **सिर्फ एडमिन ही /cancel कमांड चला सकते हैं!**")

    tagging_enabled[chat_id] = False
    await message.reply_text("✅ **Tagging को बंद कर दिया गया है!**")

print("✅ Tag Bot Loaded Successfully!")
