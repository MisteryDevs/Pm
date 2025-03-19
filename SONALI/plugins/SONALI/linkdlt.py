from SONALI import app
from pyrogram import filters

# Link delete settings
linkdlt_status = {}

async def get_owner_id(chat_id):
    chat = await app.get_chat(chat_id)
    return chat.creator.id if chat.creator else None

@app.on_message(filters.group & filters.command(["linkdlt"]))
async def toggle_linkdlt(client, message):
    owner_id = await get_owner_id(message.chat.id)

    if owner_id is None:
        return await message.reply("❌ **Owner ID not found!**")
    
    if message.from_user.id != owner_id:
        return await message.reply("❌ **Only the group owner can use this command!**")

    if len(message.command) < 2:
        return await message.reply("⚠️ **Usage:** `/linkdlt on` OR `/linkdlt off`")

    mode = message.command[1].lower()

    if mode == "on":
        linkdlt_status[message.chat.id] = True
        await message.reply("✅ **Link deletion enabled!**")

    elif mode == "off":
        linkdlt_status[message.chat.id] = False
        await message.reply("❌ **Link deletion disabled!**")

    else:
        await message.reply("⚠️ **Invalid command!** Use `/linkdlt on` OR `/linkdlt off`")

@app.on_message(filters.group & filters.text)
async def delete_links(client, message):
    """Delete links only if /linkdlt is on"""
    if not linkdlt_status.get(message.chat.id, False):
        return

    owner_id = await get_owner_id(message.chat.id)

    if owner_id and "http" in message.text:
        if message.from_user.id == owner_id:
            return
        await message.delete()
        await message.reply("⚠️ **Links are not allowed!**")
