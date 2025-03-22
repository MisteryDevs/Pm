from SONALI import app
from pyrogram import filters
import asyncio

# Default edit delete time (1 min)
edit_delete_time = 60  
edit_protection = False  # By default edit protection off

@app.on_message(filters.command("edit on") & filters.group)
async def edit_on(client, message):
    global edit_protection
    if not message.from_user:
        return
    
    # 4 time options for deletion
    keyboard = [
        [{"text": "1 Min", "callback_data": "set_time_60"}],
        [{"text": "5 Min", "callback_data": "set_time_300"}],
        [{"text": "10 Min", "callback_data": "set_time_600"}],
        [{"text": "20 Min", "callback_data": "set_time_1200"}]
    ]
    
    edit_protection = True
    await message.reply_text("🛑 *Edit Protection Enabled!*\n\n⏳ Select the time after which edited messages will be deleted:", reply_markup={"inline_keyboard": keyboard})
    
@app.on_message(filters.command("edit off") & filters.group)
async def edit_off(client, message):
    global edit_protection
    edit_protection = False
    await message.reply_text("❌ *Edit Protection Disabled!*")

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    global edit_delete_time
    data = callback_query.data
    
    if data.startswith("set_time_"):
        edit_delete_time = int(data.split("_")[2])  # Extract time
        await callback_query.message.edit_text(f"✅ Edit Protection Set to {edit_delete_time // 60} Min!")

@app.on_edited_message(filters.group)
async def delete_edited_message(client, message):
    global edit_protection, edit_delete_time
    if not edit_protection:
        return  # If edit protection is off, do nothing

    # Send warning message
    warning_msg = await message.reply_text(f"⚠️ *Your edited message will be deleted in {edit_delete_time // 60} minutes!*")
    
    await asyncio.sleep(edit_delete_time)  # Wait for set time
    await message.delete()  # Delete edited message
    await warning_msg.delete()  # Delete warning message

print("Bot is Running...")
app.run()
