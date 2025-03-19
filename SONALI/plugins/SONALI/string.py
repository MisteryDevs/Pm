import asyncio
from pyrogram import Client, filters
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded
)
from SONALI import app  

async def generate_session(client, message):
    user_id = message.from_user.id

    try:
        # ✅ Step 1: API ID
        await message.reply_text("📢 **String Session Generator**\n\n💡 Send Your **API ID (Number)**:")
        api_id_msg = await client.listen(user_id)
        api_id = api_id_msg.text.strip()

        if not api_id.isdigit():
            return await message.reply_text("❌ **Invalid API ID! Must be a number.**")

        api_id = int(api_id)  # Convert to integer

        # ✅ Step 2: API HASH
        await message.reply_text("🔑 **Send Your API HASH (32 characters, lowercase):**")
        api_hash_msg = await client.listen(user_id)
        api_hash = api_hash_msg.text.strip()

        if len(api_hash) != 32 or not api_hash.isalnum():
            return await message.reply_text("❌ **Invalid API HASH! Must be 32 alphanumeric characters.**")

        # ✅ Step 3: Phone Number
        await message.reply_text("📞 **Send Your Phone Number (With Country Code, e.g., +919876543210):**")
        phone_msg = await client.listen(user_id)
        phone_number = phone_msg.text.strip()

        if not phone_number.startswith("+") or not phone_number[1:].isdigit():
            return await message.reply_text("❌ **Invalid Phone Number! Must start with `+` and be digits.**")

        # ✅ Creating Pyrogram Client
        new_client = Client("string_session", api_id=api_id, api_hash=api_hash)

        await new_client.connect()

        try:
            sent_code = await new_client.send_code(phone_number)
            phone_code_hash = sent_code.phone_code_hash
        except PhoneNumberInvalid:
            return await message.reply_text("❌ **Invalid Phone Number! Please check and try again.**")

        # ✅ Step 4: OTP Verification
        await message.reply_text("📩 **Enter OTP as Space-Separated (e.g. 1 2 3 4 5):**")
        otp_msg = await client.listen(user_id)
        phone_code = otp_msg.text.replace(" ", "").strip()

        try:
            # 🛠️ FIXED: Correctly passing `phone_code_hash`
            await new_client.sign_in(phone_number, phone_code, phone_code_hash=phone_code_hash)
        except PhoneCodeInvalid:
            return await message.reply_text("❌ **Invalid OTP! Please check and try again.**")
        except PhoneCodeExpired:
            return await message.reply_text("❌ **OTP Expired! Please restart the process.**")
        except SessionPasswordNeeded:
            await message.reply_text("🔐 **Your Account has 2FA Enabled! Send Your Password:**")
            password_msg = await client.listen(user_id)
            password = password_msg.text.strip()
            await new_client.check_password(password)

        # ✅ Generating Session String
        session_string = await new_client.export_session_string()
        await new_client.send_message("me", f"✅ **Your Telegram String Session:**\n\n```{session_string}```\n\n⚠ **Keep It Safe!**")
        await message.reply_text("✅ **Session Generated & Sent to Your Saved Messages!**")

    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{str(e)}`")

    await new_client.disconnect()

# 🔥 Command: /string
@app.on_message(filters.command("string") & filters.private)
async def start_string_session(client, message):
    await generate_session(client, message)
