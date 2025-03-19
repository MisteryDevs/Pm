import asyncio
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded

# ✅ Tumhara existing bot
from SONALI import app  

async def generate_session(client, message):
    user_id = message.from_user.id
    try:
        await message.reply_text("📢 **String Session Generator**\n\n💡 Send Your **API ID**:")

        # API ID Input
        api_id_msg = await client.listen(user_id)
        api_id = api_id_msg.text.strip()

        await message.reply_text("🔑 **Send Your API HASH:**")

        # API HASH Input
        api_hash_msg = await client.listen(user_id)
        api_hash = api_hash_msg.text.strip()

        await message.reply_text("📞 **Send Your Phone Number (With Country Code):**")

        # Phone Number Input
        phone_msg = await client.listen(user_id)
        phone_number = phone_msg.text.strip()

        new_client = Client("string_session", api_id=int(api_id), api_hash=api_hash)

        await new_client.connect()
        sent_code = await new_client.send_code(phone_number)
        phone_code_hash = sent_code.phone_code_hash

        await message.reply_text("📩 **Enter OTP as Space-Separated (e.g. 1 2 3 4 5):**")

        # OTP Input (Space-separated fix)
        otp_msg = await client.listen(user_id)
        phone_code = otp_msg.text.replace(" ", "").strip()

        try:
            await new_client.sign_in(phone_number, phone_code, phone_code_hash=phone_code_hash)
        except SessionPasswordNeeded:
            await message.reply_text("🔐 **Your Account has 2FA Enabled! Send Your Password:**")
            password_msg = await client.listen(user_id)
            password = password_msg.text.strip()
            await new_client.check_password(password)

        # ✅ Generate String Session
        session_string = await new_client.export_session_string()

        # 📩 Save Messages me send karega
        await new_client.send_message("me", f"✅ **Here is Your Telegram String Session:**\n\n```{session_string}```\n\n⚠ **Keep It Safe!**")
        await message.reply_text("✅ **Session Generated & Sent to Your Saved Messages!**")

    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{str(e)}`")

    await new_client.disconnect()

# ✅ /string command handler
@app.on_message(filters.command("string") & filters.private)
async def start_string_session(client, message):
    await generate_session(client, message)
