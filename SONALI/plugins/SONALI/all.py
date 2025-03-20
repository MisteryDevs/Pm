from pyrogram import filters
from pyrogram.types import Message
from SONALI import app  # तुम्हारे बॉट का इम्पोर्ट

@app.on_message(filters.command("all") & filters.group)
async def tag_all(client, message: Message):
    chat_id = message.chat.id

    # सिर्फ एडमिन्स ही कमांड यूज़ कर सकते हैं
    admins = [admin.user.id async for admin in client.get_chat_members(chat_id, filter="administrators")]
    if message.from_user.id not in admins:
        return await message.reply_text("🚫 **सिर्फ एडमिन्स इस कमांड को यूज़ कर सकते हैं!**")

    # ग्रुप मेंबर लिस्ट लो
    members = [member.user.id async for member in client.get_chat_members(chat_id)]

    # एक मैसेज में 5 यूज़र्स को टैग करो
    tagged_users = []
    for user_id in members:
        tagged_users.append(f"[‌‍👤](tg://user?id={user_id})")
        if len(tagged_users) == 5:
            await message.reply_text(" ".join(tagged_users))
            tagged_users = []  # लिस्ट क्लियर करो

    # अगर लास्ट में कुछ बचा हो, तो उसे भी भेजो
    if tagged_users:
        await message.reply_text(" ".join(tagged_users))
