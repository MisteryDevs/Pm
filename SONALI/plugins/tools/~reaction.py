from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from SONALI import app

# Reaction system ka status (default: enabled)
reaction_enabled = True

# Admins ke liye command
@app.on_message(filters.command(["reaction"]) & filters.group)
async def toggle_reaction(client: Client, message: Message):
    global reaction_enabled

    # Check if user is admin
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await client.get_chat_member(chat_id, user_id)
    
    if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        return await message.reply("❌ **Sirf Admin hi is command ka use kar sakte hain!**")

    # Toggle reaction system
    if len(message.command) > 1:
        action = message.command[1].lower()
        if action == "on":
            reaction_enabled = True
            return await message.reply("✅ **Reaction System Enabled!**")
        elif action == "off":
            reaction_enabled = False
            return await message.reply("❌ **Reaction System Disabled!**")
    
    # Agar koi argument na ho to usage dikhaye
    await message.reply("⚙️ **Usage:** `/reaction on` ya `/reaction off`")


# Auto-reactions (Har jagah kaam karega)
@app.on_message(filters.incoming)
async def react_to_messages(client: Client, message: Message):
    global reaction_enabled
    if not reaction_enabled:
        return  # Agar disabled hai to react mat karo
    
    try:
        reactions = ["👍", "🙂", "🙏", "👀", "🥰"]  # Multiple reactions list
        for reaction in reactions:
            await message.react(reaction)  # Har reaction bheje
    except Exception as e:
        print(f"Reaction error: {e}")
