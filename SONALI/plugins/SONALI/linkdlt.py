from SONALI import app
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
import re

# Link detect karne ke liye regex pattern
LINK_PATTERN = r"(https?://\S+|www\.\S+)"

# Ye dictionary har group ka status store karegi
linkdlt_status = {}

async def get_owner_id(chat_id):
    """Group ka owner ID fetch karega"""
    async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.status == "creator":  # Owner check karo
            return member.user.id
    return None

@app.on_message(filters.group & filters.command(["linkdlt"]))
async def toggle_linkdlt(client, message):
    """Group owner /linkdlt on ya /linkdlt off se feature enable/disable kar sakta hai"""
    
    owner_id = await get_owner_id(message.chat.id)
    
    if message.from_user.id != owner_id:
        return await message.reply("❌ **Only the group owner can use this command!**")

    # Command ka argument check karo
    if len(message.command) < 2:
        return await message.reply("⚠️ **Usage:** `/linkdlt on` OR `/linkdlt off`")
    
    mode = message.command[1].lower()
    
    if mode == "on":
        linkdlt_status[message.chat.id] = True
        await message.reply("✅ **Link deletion enabled!** Now, all links except owner's will be deleted.")
    
    elif mode == "off":
        linkdlt_status[message.chat.id] = False
        await message.reply("❌ **Link deletion disabled!** Now, links are allowed in the group.")
    
    else:
        await message.reply("⚠️ **Invalid command!** Use `/linkdlt on` OR `/linkdlt off`")

@app.on_message(filters.group & filters.text)
async def delete_links(client, message):
    """Agar /linkdlt on hai tabhi links delete honge"""
    
    if not linkdlt_status.get(message.chat.id, False):
        return  # Agar OFF hai to kuch nahi karega

    owner_id = await get_owner_id(message.chat.id)

    if owner_id and re.search(LINK_PATTERN, message.text):  # Message me link check karo
        if message.from_user.id == owner_id:  # Agar owner hai to allow
            return
        else:
            await message.delete()  # Message delete karo
            await message.reply("⚠️ **Links are not allowed in this group!**", quote=True)
