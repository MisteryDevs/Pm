import time
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch
import config
from SONALI import app
from SONALI.misc import _boot_
from SONALI.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from SONALI.utils.decorators.language import LanguageStart
from SONALI.utils.formatters import get_readable_time
from SONALI.utils.inline import private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_comm(client, message: Message, _):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)

    # 🕊️ Auto Reaction on /start
    await message.react("🕊️")

    # 🎭 Typing Effect - Ding Dong
    try:
        vip = await message.reply_text("**ᴅιиg ᴅσиg ꨄ︎❣️.....**")
        for i in range(5):
            await vip.edit_text(f"**ᴅιиg ᴅσиg ꨄ︎{'.' * (5-i)}❣️{'.' * i}**")
            await asyncio.sleep(0.2)
        await vip.delete()

        # 🎭 Typing Effect - "Starting..."
        vips = await message.reply_text("**⚡ѕ**")
        steps = ["**⚡ѕт**", "**⚡ѕтα**", "**⚡ѕтαя**", "**⚡ѕтαят**", "**⚡ѕтαятι**", 
                 "**⚡ѕтαятιи**", "**⚡ѕтαятιиg**", "**⚡ѕтαятιиg.**", "**⚡ѕтαятιиg....**"]
        for step in steps:
            await asyncio.sleep(0.1)
            await vips.edit_text(step)
        await asyncio.sleep(0.2)
        await vips.delete()

        # 🎭 Sticker Send & Delete (1 sec)
        sticker = await client.send_sticker(
            chat_id=chat_id,
            sticker="CAACAgUAAx0CcSyO9gACl7dkQoL0p1vXqcYtCuCHmSyh4Hi1UgACEwgAAonAEVYwaJ0Jkk8L0B4E"
        )
        await asyncio.sleep(1)
        await sticker.delete()

    except Exception as e:
        print(f"Error in animation: {e}")

    # 🔥 Continue /start Logic After Animation
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name.startswith("help"):
            keyboard = InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help", close=True)
            )
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            results = VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=_["S_B_8"], url=link),
                  InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT)]]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} checked <b>Track Information</b>.\n\n"
                         f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                         f"<b>Username:</b> @{message.from_user.username}",
                )
                return

    out = private_panel(_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )

    if await is_on_off(2):
        await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} started the bot.\n\n"
                 f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                 f"<b>Username:</b> @{message.from_user.username}",
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
