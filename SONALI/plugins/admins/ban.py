import asyncio
import datetime
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired, UserAdminInvalid, BadRequest
)

from SONALI import app  # Ensure this is correctly set up

# Function to mention a user
def mention(user_id, name, mention=True):
    if mention:
        return f"[{name}](tg://user?id={user_id})"
    return name

# Get user ID from username
async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
        return [user.id, user.first_name]
    except Exception:
        return None

# Ban user function
async def ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason=None, time=None):
    try:
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "Ban rights? Nah, I'm just here for the digital high-fives 🙌\nGive me ban rights! 😡🥺", False
    except UserAdminInvalid:
        return "I won’t ban an admin, bruh!!", False
    except Exception as e:
        if user_id == app.me.id:
            return "Why should I ban myself? Sorry, but I'm not stupid like you.", False
        return f"Oops!!\n{e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    msg_text = f"{user_mention} was banned by {admin_mention}\n"
    
    if reason:
        msg_text += f"Reason: `{reason}`\n"
    if time:
        msg_text += f"Time: `{time}`\n"
    
    return msg_text, True

# Unban user function
async def unban_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "I need unban rights! 😡🥺"
    except Exception as e:
        return f"Oops!!\n{e}"

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    return f"{user_mention} was unbanned by {admin_mention}"

# Mute user function
async def mute_user(user_id, first_name, admin_id, admin_name, chat_id, reason=None, time=None):
    try:
        mute_end_time = datetime.datetime.now() + time if time else None
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), until_date=mute_end_time)
    except ChatAdminRequired:
        return "Mute rights? Nah, I need mute rights! 😡🥺", False
    except UserAdminInvalid:
        return "I won’t mute an admin, bruh!!", False
    except Exception as e:
        if user_id == app.me.id:
            return "Why should I mute myself? Sorry, but I'm not stupid like you.", False
        return f"Oops!!\n{e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    msg_text = f"{user_mention} was muted by {admin_mention}\n"
    
    if reason:
        msg_text += f"Reason: `{reason}`\n"
    if time:
        msg_text += f"Time: `{time}`\n"
    
    return msg_text, True

# Unmute user function
async def unmute_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True))
    except ChatAdminRequired:
        return "I need unmute rights! 😡🥺"
    except Exception as e:
        return f"Oops!!\n{e}"

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    return f"{user_mention} was unmuted by {admin_mention}"

# Timed mute function
@app.on_message(filters.command(["tmute"]))
async def tmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("You don’t have permission to mute someone")

    if not member.privileges.can_restrict_members:
        return await message.reply_text("You don’t have permission to mute someone")

    if not message.reply_to_message or len(message.command) < 2:
        return await message.reply_text("Please reply to a user and specify the mute duration (e.g., `/tmute 2m`)")

    user_id = message.reply_to_message.from_user.id
    first_name = message.reply_to_message.from_user.first_name
    time_text = message.command[1]

    try:
        time_amount = int(time_text[:-1])  # Extract number
        time_unit = time_text[-1]  # Extract unit
    except ValueError:
        return await message.reply_text("Invalid format! Use `/tmute 2m` (minutes), `/tmute 1h` (hours), `/tmute 1d` (days)")

    if time_unit == "m":
        mute_duration = datetime.timedelta(minutes=time_amount)
    elif time_unit == "h":
        mute_duration = datetime.timedelta(hours=time_amount)
    elif time_unit == "d":
        mute_duration = datetime.timedelta(days=time_amount)
    else:
        return await message.reply_text("Invalid format! Use:\nm = minutes\nh = hours\nd = days")

    msg_text, result = await mute_user(user_id, first_name, admin_id, admin_name, chat_id, time=mute_duration)
    await message.reply_text(msg_text)
