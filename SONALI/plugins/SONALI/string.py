import asyncio
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded

# ✅ Bot Client (Ye tumhara existing bot hai)
from SONALI import app  

async def generate_session(client, message):
    await message.reply_text("📢 **Telegram String Session Generator**\n\n📌 **Send Your API ID**")

    # API ID Input
    api_id_msg = await client.listen(message.chat.id)
    api_id = api_id_msg.text.strip()

    await message.reply_text("🔑 **Send Your API HASH**")
    
    # API HASH Input
    api_hash_msg = await client.listen(message.chat.id)
    api_hash = api_hash_msg.text.strip()

    await message.reply_text("📞 **Send Your Phone Number (With Country Code):**")

    # Phone Number Input
    phone_msg = await client.listen(message.chat.id)
    phone_number = phone_msg.text.strip()

    new_client = Client("string_session", api_id=int(api_id), api_hash=api_hash)

    try:
        await new_client.connect()
        sent_code = await new_client.send_code(phone_number)
        phone_code_hash = sent_code.phone_code_hash

        await message.reply_text("📩 **Enter the OTP You Received:**")

        # OTP Input
        otp_msg = await client.listen(message.chat.id)
        phone_code = otp_msg.text.strip()

        try:
            await new_client.sign_in(phone_number, phone_code, phone_code_hash=phone_code_hash)
        except SessionPasswordNeeded:
            await message.reply_text("🔐 **Enter Your 2FA Password:**")
            password_msg = await client.listen(message.chat.id)
            password = password_msg.text.strip()
            await new_client.check_password(password)

        # String Session Generate Karna
        session_string = await new_client.export_session_string()
        await message.reply_text("✅ **Here is Your Telegram String Session:**\n\n```{}```\n\n⚠ **Keep It Safe!**".format(session_string))
    
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

    await new_client.disconnect()

# ✅ /string command handler
@app.on_message(filters.command("string") & filters.private)
async def start_string_session(client, message):
    await generate_session(client, message)
