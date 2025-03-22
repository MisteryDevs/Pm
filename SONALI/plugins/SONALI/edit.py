from SONALI import app, MONGO_DB_URI  # Music Bot's existing MongoDB URL
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from pymongo import MongoClient
import time

# MongoDB connection using the same database as the Music Bot
client = MongoClient(MONGO_DB_URI)
db = client["MusicBot"]
edit_settings = db["edit_settings"]

# Edit delete time options (in seconds)
EDIT_TIMES = {
    "1 min": 60,
    "5 min": 300,
    "10 min": 600,
    "20 min": 1200
}

# Enable Edit Detection
@app.on_message(filters.command("edit on") & filters.group)
async def enable_edit_detection(client, message):
    chat_id = message.chat.id
    
    if edit_settings.find_one({"chat_id": chat_id}):
        await message.reply_text("🚀 **Edit detection already enabled!**")
        return
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🕐 1 Min", callback_data="edit_1"),
         InlineKeyboardButton("🕔 5 Min", callback_data="edit_5")],
        [InlineKeyboardButton("🕙 10 Min", callback_data="edit_10"),
         InlineKeyboardButton("🕛 20 Min", callback_data="edit_20")]
    ])
    
    await message.reply_text(
        "**📌 Choose the auto-delete time for edited messages:**",
        reply_markup=keyboard
    )

# Set delete time on button click
@app.on_callback_query(filters.regex("^edit_"))
async def set_edit_time(client, callback_query):
    chat_id = callback_query.message.chat.id
    option = callback_query.data.split("_")[1]
    selected_time = EDIT_TIMES[f"{option} min"]
    
    edit_settings.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"delete_time": selected_time}}, 
        upsert=True
    )

    await callback_query.message.edit_text(
        f"✅ **Edit detection enabled!**\n⏳ Messages will be deleted after **{option} min**."
    )

# Disable Edit Detection
@app.on_message(filters.command("edit off") & filters.group)
async def disable_edit_detection(client, message):
    chat_id = message.chat.id

    if not edit_settings.find_one({"chat_id": chat_id}):
        await message.reply_text("⚠️ **Edit detection is not enabled!**")
        return
    
    edit_settings.delete_one({"chat_id": chat_id})
    
    await message.reply_text("❌ **Edit detection disabled!**")

# Detect Edited Messages
@app.on_edited_message(filters.group)
async def check_message_edit(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    settings = edit_settings.find_one({"chat_id": chat_id})
    if not settings:
        return  

    delete_time = settings["delete_time"]

    # Ignore edits by sudo users & bot itself
    if user_id in [OWNER_ID] + SUDO_USERS or message.from_user.is_bot:
        return

    # Send warning & delete after time
    warning = await message.reply_text(
        f"⚠️ **{message.from_user.mention} edited a message!**\n"
        f"🔹 **Old Message:** {message.text if message.text else 'Media Edited'}\n"
        f"⏳ **Auto-deleting in {delete_time // 60} min...**"
    )
    await asyncio.sleep(delete_time)
    await message.delete()
    await warning.delete()
