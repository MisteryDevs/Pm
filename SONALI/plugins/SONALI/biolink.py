from SONALI import app
from pyrogram import filters
import time
from threading import Thread
from telebot import TeleBot, types

# Logger Group Chat ID
LOGGER_GROUP_CHAT_ID = -1002300353707

# Bot Owner User ID
OWNER_USER_ID = 7096860602

# Store User Warnings
user_bio_warnings = {}
protection_enabled = {}

# 🚀 Function to log messages in the logger group
def log_to_logger_group(log_message):
    try:
        app.send_message(LOGGER_GROUP_CHAT_ID, log_message)
    except Exception as e:
        print(f"⚠️ Logger Error: {e}")

# 🔹 Enable Bio Link Protection
@app.on_message(filters.command("biolink on") & filters.group)
def enable_protection(client, message):
    chat_id = message.chat.id
    if chat_id in protection_enabled:
        app.send_message(chat_id, "🔹 **Bio Link Protection is Already Enabled!**")
    else:
        protection_enabled[chat_id] = True
        app.send_message(chat_id, "✅ **Bio Link Protection Enabled!**\nNow I'll monitor bios for any links.")
        log_to_logger_group(f"🚀 **Bio Link Protection Enabled** in `{message.chat.title}` by `{message.from_user.first_name}`.")

# 🔹 Disable Bio Link Protection
@app.on_message(filters.command("biolink off") & filters.group)
def disable_protection(client, message):
    chat_id = message.chat.id
    if chat_id in protection_enabled:
        del protection_enabled[chat_id]
        app.send_message(chat_id, "❌ **Bio Link Protection Disabled!**\nI will no longer check bios for links.")
        log_to_logger_group(f"⚠️ **Bio Link Protection Disabled** in `{message.chat.title}` by `{message.from_user.first_name}`.")
    else:
        app.send_message(chat_id, "🔹 **Bio Link Protection is Already Disabled!**")

# 🔥 Check if a User's Bio Has a Link & Warn
@app.on_message(filters.group)
def check_bio_and_warn(client, message):
    chat_id = message.chat.id
    user = message.from_user

    if chat_id not in protection_enabled:
        return  # Stop if protection is off

    if not user or not user.id or not user.username:
        return

    try:
        member_info = client.get_chat_member(chat_id, user.id)
        bio = member_info.user.bio if member_info.user.bio else "No bio"

        if 'http://' in bio or 'https://' in bio:
            warnings = user_bio_warnings.get(user.id, 0) + 1
            user_bio_warnings[user.id] = warnings

            if warnings < 3:
                app.send_message(chat_id, f"⚠️ **Warning {warnings}/3!** @{user.username}, remove the link from your bio or you'll be muted!")
            elif warnings == 3:
                mute_user(chat_id, user.id, user.username)
    except Exception as e:
        print(f"⚠️ Error Checking Bio: {e}")

# 🚫 Mute User for 3 Hours & Add Unmute Button
def mute_user(chat_id, user_id, username):
    try:
        app.restrict_chat_member(chat_id, user_id, can_send_messages=False)
        markup = types.InlineKeyboardMarkup()
        unmute_button = types.InlineKeyboardButton("🔓 Unmute", callback_data=f"unmute_{user_id}")
        markup.add(unmute_button)

        app.send_message(chat_id, f"🚫 **User @{username} Muted for 3 Hours!** Bio link not removed.", reply_markup=markup)
        log_to_logger_group(f"🚨 **User Muted:** @{username} in `{chat_id}`")

        # Start Timer to Auto-Unmute After 3 Hours
        Thread(target=auto_unmute, args=(chat_id, user_id)).start()

    except Exception as e:
        print(f"⚠️ Mute Error: {e}")

# 🔓 Auto-Unmute User After 3 Hours
def auto_unmute(chat_id, user_id):
    time.sleep(10800)  # 3 hours
    try:
        app.restrict_chat_member(chat_id, user_id, can_send_messages=True)
        app.send_message(chat_id, f"🔓 **User Unmuted Automatically!**")
    except Exception as e:
        print(f"⚠️ Auto-Unmute Error: {e}")

# ✅ Run the Bot
print("🚀 Bio Link Protection Bot Running!")
app.run()
