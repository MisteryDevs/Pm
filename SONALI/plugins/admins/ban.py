import asyncio
import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
)

# Initialize the bot
app = Client("moderation_bot", api_id=123456, api_hash="your_api_hash", bot_token="your_bot_token")


def mention(user_id, name):
    """Returns a clickable mention link for a user."""
    return f"<a href='tg://user?id={user_id}'>{name}</a>"


async def get_userid_from_username(username):
    """Fetch user ID and first name from username."""
    try:
        user = await app.get_users(username)
        return user.id, user.first_name
    except Exception:
        return None, None


async def ban_user(chat_id, user_id, first_name, admin_id, admin_name, reason=None):
    """Bans a user from the chat."""
    try:
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "I don't have ban permissions!", False
    except UserAdminInvalid:
        return "I can't ban an admin!", False
    except Exception as e:
        return f"Error: {e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg = f"{user_mention} was banned by {admin_mention}."
    if reason:
        msg += f"\nReason: `{reason}`"
    return msg, True


async def unban_user(chat_id, user_id, first_name, admin_id, admin_name):
    """Unbans a user from the chat."""
    try:
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "I don't have unban permissions!"
    except Exception as e:
        return f"Error: {e}"

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    return f"{user_mention} was unbanned by {admin_mention}."


async def mute_user(chat_id, user_id, first_name, admin_id, admin_name, duration=None, reason=None):
    """Mutes a user for a specific duration or permanently."""
    try:
        mute_time = datetime.datetime.now() + datetime.timedelta(minutes=duration) if duration else None
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), until_date=mute_time)
    except ChatAdminRequired:
        return "I don't have mute permissions!", False
    except UserAdminInvalid:
        return "I can't mute an admin!", False
    except Exception as e:
        return f"Error: {e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg = f"{user_mention} was muted by {admin_mention}."
    if reason:
        msg += f"\nReason: `{reason}`"
    if duration:
        msg += f"\nDuration: `{duration} minutes`"

    return msg, True


# --- Commands ---

@app.on_message(filters.command("ban") & filters.group)
async def ban_command(client, message):
    """Handles the /ban command."""
    if not message.reply_to_message:
        return await message.reply("Reply to a user to ban them!")

    user_id = message.reply_to_message.from_user.id
    first_name = message.reply_to_message.from_user.first_name
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    chat_id = message.chat.id
    reason = " ".join(message.command[1:]) if len(message.command) > 1 else None

    response, success = await ban_user(chat_id, user_id, first_name, admin_id, admin_name, reason)
    if success:
        await message.reply(response, parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command("unban") & filters.group)
async def unban_command(client, message):
    """Handles the /unban command."""
    if len(message.command) < 2:
        return await message.reply("Usage: `/unban @username`")

    username = message.command[1]
    user_id, first_name = await get_userid_from_username(username)

    if not user_id:
        return await message.reply("User not found!")

    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    chat_id = message.chat.id

    response = await unban_user(chat_id, user_id, first_name, admin_id, admin_name)
    await message.reply(response, parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command("mute") & filters.group)
async def mute_command(client, message):
    """Handles the /mute command."""
    if not message.reply_to_message:
        return await message.reply("Reply to a user to mute them!")

    user_id = message.reply_to_message.from_user.id
    first_name = message.reply_to_message.from_user.first_name
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    chat_id = message.chat.id

    duration = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else None
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else None

    response, success = await mute_user(chat_id, user_id, first_name, admin_id, admin_name, duration, reason)
    if success:
        await message.reply(response, parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command("unmute") & filters.group)
async def unmute_command(client, message):
    """Handles the /unmute command."""
    if not message.reply_to_message:
        return await message.reply("Reply to a user to unmute them!")

    user_id = message.reply_to_message.from_user.id
    first_name = message.reply_to_message.from_user.first_name
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True))
        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)
        await message.reply(f"{user_mention} was unmuted by {admin_mention}.", parse_mode=enums.ParseMode.HTML)
    except ChatAdminRequired:
        await message.reply("I don't have unmute permissions!")


# --- Start the bot ---
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
