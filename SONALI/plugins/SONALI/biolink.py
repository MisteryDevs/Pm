from pyrogram import filters
import telebot
from telebot import types
import time
import datetime
from SONALI import app

API_TOKEN = '7547150081:AAHjvU21rKe6a4KJXRu7Ui3WJseUgjCk-h8'
bot = telebot.TeleBot(API_TOKEN)

# Logger Group Chat ID
LOGGER_GROUP_CHAT_ID = -1002300353707

# Bot Owner User ID
OWNER_USER_ID = 7096860602

# Store User Warnings
user_bio_warnings = {}
protection_enabled = {}

# 🚀 Function to log messages in the logger group
def log_to_logger_group(log_message):
    bot.send_message(LOGGER_GROUP_CHAT_ID, log_message)

# 🔹 Enable Bio Link Protection
@app.on_message(filters.command("biolink on") & filters.group)
def enable_protection(client, message):
    chat_id = message.chat.id
    if chat_id in protection_enabled:
        bot.send_message(chat_id, "🔹 **Bio Link Protection is Already Enabled!**")
    else:
        protection_enabled[chat_id] = True
        bot.send_message(chat_id, "✅ **Bio Link Protection Enabled!**\nNow I'll monitor bios for any links.")
        log_to_logger_group(f"🚀 **Bio Link Protection Enabled** in `{message.chat.title}` by `{message.from_user.first_name}`.")

# 🔹 Disable Bio Link Protection
@app.on_message(filters.command("biolink off") & filters.group)
def disable_protection(client, message):
    chat_id = message.chat.id
    if chat_id in protection_enabled:
        del protection_enabled[chat_id]
        bot.send_message(chat_id, "❌ **Bio Link Protection Disabled!**\nI will no longer check bios for links.")
        log_to_logger_group(f"⚠️ **Bio Link Protection Disabled** in `{message.chat.title}` by `{message.from_user.first_name}`.")
    else:
        bot.send_message(chat_id, "🔹 **Bio Link Protection is Already Disabled!**")

# 🔥 Check if a User's Bio Has a Link
def check_and_warn_users(chat_id):
    try:
        if chat_id not in protection_enabled:
            return  # Stop if protection is off

        members = bot.get_chat_members(chat_id)
        for member in members:
            member_info = bot.get_chat_member(chat_id, member.user.id)
            bio = member_info.user.bio if member_info.user.bio else "No bio"

            if 'http://' in bio or 'https://' in bio:
                bot.send_message(chat_id, f"⚠️ **Warning!** @{member.user.username}, remove the link from your bio within 1 hour or you'll be muted.")
                user_bio_warnings[member.user.id] = time.time()
                start_timer(member.user.id, chat_id)

    except Exception as e:
        print(f"⚠️ Error Checking Users: {e}")

# 🕒 Timer to Mute Users Who Don't Remove Links
def start_timer(user_id, chat_id):
    time.sleep(3600)  # Wait for 1 hour
    if user_id in user_bio_warnings and time.time() - user_bio_warnings[user_id] > 3600:
        if user_id != OWNER_USER_ID:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)
            bot.send_message(chat_id, f"🚫 **User @{user_id} Muted!** Bio link not removed in 1 hour.")
        else:
            bot.send_message(chat_id, f"⚠️ **Owner {OWNER_USER_ID} Detected - Mute Skipped!**")

# ✅ Check If Bot Has Ban Permissions
def has_ban_permission(chat_id):
    try:
        chat_member = bot.get_chat_member(chat_id, bot.get_me().id)
        return chat_member.status in ['administrator', 'creator'] and chat_member.can_restrict_members
    except Exception as e:
        print(f"⚠️ Error Checking Permissions: {e}")
        return False

# 🚀 Bot Added to Group - Enable Auto Bio Check
@bot.message_handler(content_types=['new_chat_members'])
def log_new_group(message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id == bot.get_me().id:
                log_message = f"🚀 **Bot Added!** `{message.chat.title}` by `{message.from_user.first_name}`."
                log_to_logger_group(log_message)
                check_and_warn_users(message.chat.id)

# ❌ Ban a User
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id == bot.get_me().id:
        bot.send_message(message.chat.id, "😏 **Bhai, Apne Aap Ko Kaise Ban Karu?**")
        return

    if not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ **Reply to a User to Ban!**")
        return

    banned_user = message.reply_to_message.from_user
    if banned_user.id == bot.get_me().id:
        bot.send_message(message.chat.id, "😏 **Mujhe Ban Karne Ki Koshish? Bhai Tu Thik Hai?**")
        return

    bot.kick_chat_member(message.chat.id, banned_user.id)
    bot.send_message(message.chat.id, f"🚫 **User @{banned_user.username} Banned!**")

# 🚀 Keep the Bot Running
bot.polling(non_stop=True)
