from SONALI import app
from os import environ
from pyrogram import filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup

# Define Inline Buttons (Enhanced)
BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url="https://t.me/Sweety_music09_BOT?startgroup=true")
        ],
        [
            InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴍᴜsɪᴄ", url="https://t.me/Sweety_music09_BOT"),
            InlineKeyboardButton("💬 ɢʀᴏᴜᴘ sᴜᴘᴘᴏʀᴛ", url="https://t.me/APNA_CLUB_09")
        ]
    ]
)

# Extract environment variables
chat_id_env = environ.get("CHAT_ID")
CHAT_ID = [int(x) for x in chat_id_env.split(",")] if chat_id_env else []

# Default approval state (in-memory)
APPROVAL_STATE = True  # Start with auto-approval ON

# Stylish Welcome Message
WELCOME_TEXT = (
    "🌟 ᴡᴇʟᴄᴏᴍᴇ, {mention}! 🌟\n\n"
    "🎶 ᴛᴏ ➥ {title} 🎵\n\n"
    "💖 ʏᴏᴜ'ᴠᴇ ʙᴇᴇɴ ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇᴅ! 🎉\n"
    "✨ ᴇɴᴊᴏʏ ᴍᴜsɪᴄ & ɢʀᴏᴏᴠᴇ ʟɪᴋᴇ ɴᴇᴠᴇʀ ʙᴇғᴏʀᴇ! ✨\n\n"
    "📌 ᴄᴏᴍᴍᴀɴᴅs ➥ /play, /pause, /skip, /stop**\n"
    "📌 ɢᴇᴛ sᴜᴘᴘᴏʀᴛ ➥ @SweetyMusicSupport**\n\n"
    "🔥 ʟᴇᴛ'ꜱ  ᴍᴀᴋᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴍᴏʀᴇ ᴍᴜsɪᴄᴀʟ!** 🔥"
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
@app.on_message(filters.command("approveon") & filters.group)
async def enable_autoapprove(client, message):
    global APPROVAL_STATE
    APPROVAL_STATE = True
    await message.reply_text("✅ Auto-approval has been ENABLED!\nNew join requests will be approved automatically.")

# Command to Disable Auto-Approval
@app.on_message(filters.command("approveoff") & filters.group)
async def disable_autoapprove(client, message):
    global APPROVAL_STATE
    APPROVAL_STATE = False
    await message.reply_text("❌ Auto-approval has been DISABLED!\nAdmins must manually approve new join requests.")
