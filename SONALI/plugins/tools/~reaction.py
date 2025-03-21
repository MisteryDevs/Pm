import random
from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI import app

# Reaction System ON/OFF Storage
reaction_status = {}

# Reaction List
reactions = ["👍", "🙂", "🙏", "👀", "🥰"]

# ✅ Automatically React to All Messages (Groups, Channels, DMs)
@app.on_message(filters.all)
async def react_to_messages(client: Client, message: Message):
    chat_id = message.chat.id

    # Agar reaction disabled hai to kuch nahi karega
    if reaction_status.get(chat_id, True) is False:
        return  

    try:
        reaction = random.choice(reactions)  # Random Reaction Select
        await message.react(reaction)
    except Exception as e:
        print(f"Failed to react to message: {e}")

# ✅ Admins Only - Toggle Reaction ON/OFF
@app.on_message(filters.command("reaction") & filters.group)
async def toggle_reaction(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ✅ Check if User is Admin
    chat_member = await client.get_chat_member(chat_id, user_id)
    if chat_member.status not in ["administrator", "creator"]:
        return await message.reply_text("❌ **Sirf Admins hi Reaction System ON/OFF kar sakte hain!**")

    # ✅ Toggle Reaction System
    reaction_status[chat_id] = not reaction_status.get(chat_id, True)
    status = "✅ Enabled" if reaction_status[chat_id] else "❌ Disabled"
    await message.reply_text(f"**Reaction System:** {status}")
