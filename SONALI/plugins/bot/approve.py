from SONALI import app
from os import environ
from pyrogram import filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup, Message

# Define Inline Button (Only Add Me)
BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(" ➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url="https://t.me/Sweety_music09_BOT?startgroup=true")
        ]
    ]
)

# Default approval state (in-memory)
APPROVAL_STATE = True  # Start with auto-approval ON

# Stylish Welcome Message
WELCOME_TEXT = (
    "🌟 ᴡᴇʟᴄᴏᴍᴇ, {mention}! 🌟\n\n"
    "🎶 ᴛᴏ ➥ {title} 🎵\n\n"
    "💖 ʏᴏᴜ'ᴠᴇ ʙᴇᴇɴ ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇᴅ! 🎉\n"
    "✨ ᴇɴᴊᴏʏ ᴍᴜsɪᴄ & ɢʀᴏᴏᴠᴇ ʟɪᴋᴇ ɴᴇᴠᴇʀ ʙᴇғᴏʀᴇ! ✨\n"
)

# Auto-Approval Event Handler
@app.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client, message: ChatJoinRequest):
    global APPROVAL_STATE  # Use global variable for approval state

    chat = message.chat  # Target Chat
    user = message.from_user  # Joining User

    print(f"✅ {user.first_name} ({user.id}) requested to join '{chat.title}' ({chat.id})")

    # Check if auto-approval is enabled
    if APPROVAL_STATE:
        # Approve Join Request
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)

        # Send Welcome Message
        await client.send_message(
            chat_id=chat.id,
            text=WELCOME_TEXT.format(mention=user.mention, title=chat.title),
            reply_markup=BUTTONS
        )

# Command to Enable Auto-Approval
@app.on_message(filters.command("approve on") & (filters.group | filters.channel))
async def enable_autoapprove(client, message: Message):
    global APPROVAL_STATE
    APPROVAL_STATE = True
    await message.reply_text("✅ ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇʟ ᴇɴᴀʙʟᴇᴅ!\nNew ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛs ᴡɪʟʟ ʙᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.")

# Command to Disable Auto-Approval
@app.on_message(filters.command("approve off") & (filters.group | filters.channel))
async def disable_autoapprove(client, message: Message):
    global APPROVAL_STATE
    APPROVAL_STATE = False
    await message.reply_text("❌ Aᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇ ᴅɪsᴀʙʟᴇᴅ !\nAᴅᴍɪɴs ᴍᴜsᴛ ᴍᴀɴᴜᴀʟʟʏ ᴀᴘᴘʀᴏᴠᴇ ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛs.")
