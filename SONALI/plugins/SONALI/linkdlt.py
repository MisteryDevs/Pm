from SONALI import app
from pyrogram import filters
import re

# Link detect karne ke liye regex pattern
LINK_PATTERN = r"(https?://\S+|www\.\S+)"

async def get_owner_id(chat_id):
    """Group ka owner ID fetch karega"""
    group_owner = await app.get_chat(chat_id)
    return group_owner.owning_user.id

@app.on_message(filters.group & filters.text)
async def delete_links(client, message):
    """Agar koi user ya admin link bhejta hai to delete karega, sirf owner ke alawa"""
    
    owner_id = await get_owner_id(message.chat.id)

    if re.search(LINK_PATTERN, message.text):  # Message me link check karo
        if message.from_user.id == owner_id:  # Agar owner hai to allow
            return
        else:
            await message.delete()  # Message delete karo
            await message.reply("⚠️ **Links are not allowed in this group!**", quote=True)
