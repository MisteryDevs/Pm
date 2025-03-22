from SONALI import app
from pyrogram import filters
import asyncio
import os

# OWNER_ID सेट करें
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# डिफ़ॉल्ट एडिट डिलीट समय (1 मिनट)
edit_delete_time = 60  
edit_protection = False  # डिफ़ॉल्ट रूप से एडिट प्रोटेक्शन बंद

@app.on_message(filters.command("edit on") & filters.group)
async def edit_on(client, message):
    global edit_protection
    if not message.from_user:
        return

    # एडमिन या OWNER_ID ही सेट कर सके
    if message.from_user.id != OWNER_ID and not message.from_user.is_admin:
        await message.reply_text("❌ *केवल एडमिन या ओनर इस कमांड का उपयोग कर सकते हैं!*")
        return
    
    keyboard = [
        [{"text": "1 Min", "callback_data": "set_time_60"}],
        [{"text": "5 Min", "callback_data": "set_time_300"}],
        [{"text": "10 Min", "callback_data": "set_time_600"}],
        [{"text": "20 Min", "callback_data": "set_time_1200"}]
    ]
    
    edit_protection = True
    await message.reply_text(
        "🛑 *Edit Protection Enabled!*\n\n⏳ Select the time after which edited messages will be deleted:", 
        reply_markup={"inline_keyboard": keyboard}
    )

@app.on_message(filters.command("edit off") & filters.group)
async def edit_off(client, message):
    global edit_protection
    if not message.from_user:
        return
    
    if message.from_user.id != OWNER_ID and not message.from_user.is_admin:
        await message.reply_text("❌ *केवल एडमिन या ओनर इस कमांड का उपयोग कर सकते हैं!*")
        return
    
    edit_protection = False
    await message.reply_text("❌ *Edit Protection Disabled!*")

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    global edit_delete_time
    data = callback_query.data
    
    if data.startswith("set_time_"):
        edit_delete_time = int(data.split("_")[2])  # समय निकालें
        await callback_query.message.edit_text(f"✅ Edit Protection Set to {edit_delete_time // 60} Min!")

@app.on_edited_message(filters.group)
async def delete_edited_message(client, message):
    global edit_protection, edit_delete_time
    if not edit_protection:
        return  # यदि एडिट प्रोटेक्शन बंद है, तो कुछ न करें

    # चेतावनी संदेश भेजें
    warning_msg = await message.reply_text(f"⚠️ *आपका संपादित संदेश {edit_delete_time // 60} मिनट में हटा दिया जाएगा!*")
    
    await asyncio.sleep(edit_delete_time)  # निर्दिष्ट समय तक प्रतीक्षा करें
    await message.delete()  # संपादित संदेश हटाएं
    await warning_msg.delete()  # चेतावनी संदेश हटाएं

print("Bot is Running...")
app.run()
