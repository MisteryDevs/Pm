import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from SONALI import userbot as us, app
from SONALI.core.userbot import assistants


async def get_user_info(client, message):
    """ Extract user ID from message or reply """
    if not message.reply_to_message and len(message.text.split()) < 2:
        return None, (
            "✦ <b>Usage:</b>\n"
            "➤ <code>/sg @username</code> - Username se search kare\n"
            "➤ <code>/sg user_id</code> - User ID se search kare\n"
            "➤ Reply karke <code>/sg</code> likhein - Reply wale user ki info lene ke liye"
        )
    args = message.reply_to_message.from_user.id if message.reply_to_message else message.text.split()[1]
    try:
        user = await client.get_users(args)
        return user, None
    except Exception:
        return None, "✦ <code>Invalid username or ID! Please provide a valid user.</code>"


@app.on_message(filters.command(["sg", "history", "info", "userinfo"]))
async def sangmata_response(client: Client, message: Message):
    """ Fetch full response from Sangmata bot """
    user, error = await get_user_info(client, message)
    if error:
        return await message.reply(error)

    lol = await message.reply("🧨 Searching...")

    bots = ["sangmata_bot", "sangmata_beta_bot"]
    sg_bot = random.choice(bots)

    if not assistants:
        return await lol.edit("✦ <code>No assistant bots are available.</code>")

    ubot = us.one

    try:
        a = await ubot.send_message(sg_bot, str(user.id))
        await asyncio.sleep(2)

        history_text = ""
        async for stalk in ubot.search_messages(sg_bot):
            if stalk.text:
                history_text += f"{stalk.text}\n\n"

        if history_text:
            await message.reply(f"🔍 Sangmata Response:\n\n{history_text}")
        else:
            await message.reply("✦ <code>The bot did not return any information.</code>")

        # Clear chat history with the bot
        await ubot.send(DeleteHistory(peer=sg_bot, max_id=0, revoke=True))

    except Exception as e:
        return await lol.edit(f"✦ <code>Error:</code> {e}")

    await lol.delete()
