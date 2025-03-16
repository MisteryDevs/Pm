import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from SONALI import userbot as us, app
from SONALI.core.userbot import assistants


@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    if not message.reply_to_message and len(message.text.split()) < 2:
        return await message.reply(
            "✦ <b>Usage:</b>\n"
            "➤ <code>/sg @username</code> - Username se search kare\n"
            "➤ <code>/sg user_id</code> - User ID se search kare\n"
            "➤ Tag karke <code>/sg</code> likhein - Tag wale user ki info lene ke liye"
        )

    args = message.reply_to_message.from_user.id if message.reply_to_message else message.text.split()[1]

    lol = await message.reply("🧨 Searching...")

    try:
        user = await client.get_users(args)
    except Exception:
        return await lol.edit("✦ <code>Invalid username or ID! Please provide a valid user.</code>")

    bots = ["sangmata_bot", "sangmata_beta_bot"]
    sg_bot = random.choice(bots)

    if not assistants:  # Ensure there is at least one assistant
        return await lol.edit("✦ <code>No assistant bots are available.</code>")

    ubot = us.one  # Assuming `us.one` is an active userbot session

    try:
        a = await ubot.send_message(sg_bot, str(user.id))
        await asyncio.sleep(2)  # Allow time for the bot to respond

        async for stalk in ubot.search_messages(sg_bot):
            if stalk.text:
                await message.reply(stalk.text)
                break
        else:
            await message.reply("✦ <code>The bot did not return any information.</code>")

        # Clear chat history with the bot
        await ubot.send(DeleteHistory(peer=sg_bot, max_id=0, revoke=True))

    except Exception as e:
        return await lol.edit(f"✦ <code>Error:</code> {e}")

    await lol.delete()
