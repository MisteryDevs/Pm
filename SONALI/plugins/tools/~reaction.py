from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from SONALI import app

# Default: Reaction system OFF
reaction_enabled = {}

# Admins ke liye command
@app.on_message(filters.command(["reaction"]) & (filters.group | filters.channel | filters.private))
async def toggle_reaction(client: Client, message: Message):
    global reaction_enabled
    chat_id = message.chat.id

    # Agar message.from_user None ho, to ignore karein (bot messages ke case me)
    if not message.from_user:
        return
    
    # Check if user is admin (Group & Channel)
    if message.chat.type in ["supergroup", "group", "channel"]:
        user_id = message.from_user.id
        member = await client.get_chat_member(chat_id, user_id)
        
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply("❌ sɪʀғ ᴀᴅᴍɪɴ ʜɪ ɪs ᴄᴏᴍᴍɴᴅ ᴋᴀ ᴜsᴇ ᴋᴀʀsᴀᴋᴛᴇ ʜᴀɪɴ !")

    # Toggle reaction system
    if message.command and len(message.command) > 1:
        action = message.command[1].lower()
        if action == "on":
            reaction_enabled[chat_id] = True
            return await message.reply("✅ ʀᴇᴀᴄᴛɪᴏɴ sʏsᴛᴇᴍ ᴇɴᴀʙʟᴇᴅ")
        elif action == "off":
            reaction_enabled[chat_id] = False
            return await message.reply("❌ ʀᴇᴀᴄᴛɪᴏɴ sʏsᴛᴇᴍ ᴅɪsᴀʙʟᴇᴅ")
    
    # Agar koi argument na ho to usage dikhaye
    await message.reply("⚙️ ᴜsᴀɢᴇ : `/reaction on` ya `/reaction off`")


# Auto-reactions (Default: OFF)
@app.on_message(filters.incoming & (filters.group | filters.channel | filters.private))
async def react_to_messages(client: Client, message: Message):
    global reaction_enabled
    chat_id = message.chat.id
    
    if not reaction_enabled.get(chat_id, False):
        return  # Agar disabled hai to react mat karo
    
    try:
        reactions = ["👍", "🙂", "🙏", "👀", "🥰"]  # Multiple reactions list
        for reaction in reactions:
            await message.react(reaction)  # Har reaction bheje
    except Exception as e:
        print(f"Reaction error: {e}")
