import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SONALI import app  # Importing the app from SONALI.py

# Default Edit Protection Settings
edit_delete_time = 60  # Default 1 Minute
edit_protection = False  

@app.on_message(filters.command("edit on") & filters.group)
async def edit_on(client, message):
    global edit_protection
    if not message.from_user:
        return

    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if message.from_user.id != int(app.me.id) and chat_member.status not in ["administrator", "creator"]:
        await message.reply_text("❌ *केवल एडमिन या ओनर इस कमांड का उपयोग कर सकते हैं!*")
        return
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("1 Min", callback_data="set_time_60")],
        [InlineKeyboardButton("5 Min", callback_data="set_time_300")],
        [InlineKeyboardButton("10 Min", callback_data="set_time_600")],
        [InlineKeyboardButton("20 Min", callback_data="set_time_1200")]
    ])

    edit_protection = True
    await message.reply_text(
        "🛑 *Edit Protection Enabled!*\n\n⏳ Select the time after which edited messages will be deleted:", 
        reply_markup=keyboard
    )

@app.on_message(filters.command("edit off") & filters.group)
async def edit_off(client, message):
    global edit_protection
    if not message.from_user:
        return
    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if message.from_user.id != int(app.me.id) and chat_member.status not in ["administrator", "creator"]:
        await message.reply_text("❌ *केवल एडमिन या ओनर इस कमांड का उपयोग कर सकते हैं!*")
        return
    
    edit_protection = False
    await message.reply_text("❌ *Edit Protection Disabled!*")

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    global edit_delete_time
    data = callback_query.data
    
    if data.startswith("set_time_"):
        edit_delete_time = int(data.split("_")[2])
        await callback_query.message.edit_text(f"✅ Edit Protection Set to {edit_delete_time // 60} Min!")

@app.on_edited_message(filters.group)
async def delete_edited_message(client, message):
    global edit_protection, edit_delete_time
    if not edit_protection:
        return

    warning_msg = await message.reply_text(f"⚠️ *आपका संपादित संदेश {edit_delete_time // 60} मिनट में हटा दिया जाएगा!*")
    
    await asyncio.sleep(edit_delete_time)
    await message.delete()
    await warning_msg.delete()

# बॉट को स्टार्ट करें
print("Bot is Running...")
app.run()
