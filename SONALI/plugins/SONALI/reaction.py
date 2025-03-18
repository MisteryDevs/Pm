from pyrogram import Client, filters
from pyrogram.types import Message, ReactionTypeEmoji

# ✅ Reaction System Status Tracker
reaction_enabled = {}

# 🎭 Command: /reaction on
@Client.on_message(filters.command("reaction") & filters.group)
async def toggle_reaction(client, message: Message):
    chat_id = message.chat.id
    if len(message.command) > 1:
        action = message.command[1].lower()
        if action == "on":
            reaction_enabled[chat_id] = True
            await message.reply_text("✅ Auto Reaction **Enabled**!")
        elif action == "off":
            reaction_enabled[chat_id] = False
            await message.reply_text("❌ Auto Reaction **Disabled**!")
        else:
            await message.reply_text("⚠️ Use: `/reaction on` OR `/reaction off`")
    else:
        await message.reply_text("⚠️ Use: `/reaction on` OR `/reaction off`")

# 🔥 Auto Reaction on Messages
@Client.on_message(filters.group & ~filters.command("reaction"))
async def auto_react(client, message: Message):
    chat_id = message.chat.id
    if reaction_enabled.get(chat_id, False):  # Agar ON hai to react karega
        await message.react([ReactionTypeEmoji("🔥")])  # 🎭 Custom Reaction
