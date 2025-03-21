import random
from pyrogram import filters, Client, enums
from SONALI import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.types import ChatPermissions
from SONALI.mongo.nightmodedb import nightdb, nightmode_on, nightmode_off, get_nightchats

# Fixed Chat Permissions (Removed 'can_send_other_messages')
CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_add_web_page_previews=False,
    can_pin_messages=False,
    can_invite_users=True
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=True,
    can_add_web_page_previews=True,
    can_pin_messages=True,
    can_invite_users=True
)

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("๏ ᴇɴᴀʙʟᴇ ๏", callback_data="add_night"),
        InlineKeyboardButton("๏ ᴅɪsᴀʙʟᴇ ๏", callback_data="rm_night")
    ]
])

@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message):
    await message.reply_photo(
        photo="https://telegra.ph//file/06649d4d0bbf4285238ee.jpg",
        caption="**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**",
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^(add_night|rm_night)$"))
async def nightcb(_, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    check_night = await nightdb.find_one({"chat_id": chat_id})
    
    # Get list of admins
    administrators = [
        m.user.id async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)
    ]

    if user_id in administrators:
        if data == "add_night":
            if check_night:
                await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
            else:
                await nightmode_on(chat_id)
                await query.message.edit_caption("**๏ ᴛʜɪs ɢʀᴏᴜᴘ ᴡɪʟʟ ʙᴇ ᴄʟᴏsᴇᴅ ᴀᴛ 12ᴀᴍ [IST] ᴀɴᴅ ᴏᴘᴇɴᴇᴅ ᴀᴛ 6ᴀᴍ [IST].**")
        
        elif data == "rm_night":
            if check_night:
                await nightmode_off(chat_id)
                await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ !**")
            else:
                await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")

# Function to close chat at night
async def start_nightmode():
    schats = await get_nightchats()
    chats = [int(chat["chat_id"]) for chat in schats]

    if not chats:
        return

    for chat_id in chats:
        try:
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph//file/06649d4d0bbf4285238ee.jpg",
                caption="**ɢʀᴏᴜᴘ ɪs ᴄʟᴏsɪɴɢ, ɢᴏᴏᴅ ɴɪɢʜᴛ ᴇᴠᴇʀʏᴏɴᴇ !**"
            )
            await app.set_chat_permissions(chat_id, CLOSE_CHAT)
        except Exception as e:
            print(f"Unable to close Group {chat_id} - {e}")

# Function to open chat in the morning
async def close_nightmode():
    schats = await get_nightchats()
    chats = [int(chat["chat_id"]) for chat in schats]

    if not chats:
        return

    for chat_id in chats:
        try:
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph//file/14ec9c3ff42b59867040a.jpg",
                caption="**ɢʀᴏᴜᴘ ɪs ᴏᴘᴇɴɪɴɢ, ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴇᴠᴇʀʏᴏɴᴇ!**"
            )
            await app.set_chat_permissions(chat_id, OPEN_CHAT)
        except Exception as e:
            print(f"Unable to open Group {chat_id} - {e}")

# Scheduling the night mode
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(start_nightmode, trigger="cron", hour=18, minute=53)  # 12 AM IST
scheduler.add_job(close_nightmode, trigger="cron", hour=18, minute=54)  # 6 AM IST
scheduler.start()
