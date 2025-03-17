from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from SONALI import app
from SONALI.utils import first_page, second_page
from SONALI.utils.database import get_lang
from SONALI.utils.decorators.language import LanguageStart, languageCB
from SONALI.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        await update.answer()
        chat_id = update.message.chat.id
    else:
        chat_id = update.chat.id
        await update.delete()

    language = await get_lang(chat_id)
    _ = get_string(language)
    keyboard = first_page(_)

    if is_callback:
        await update.edit_message_text(_["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard)
    else:
        await update.reply_photo(photo=START_IMG_URL, caption=_["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard)

@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    help_dict = {
        "hb1": helpers.HELP_1, "hb2": helpers.HELP_2, "hb3": helpers.HELP_3, "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5, "hb6": helpers.HELP_6, "hb7": helpers.HELP_7, "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9, "hb10": helpers.HELP_10, "hb11": helpers.HELP_11, "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13, "hb14": helpers.HELP_14, "hb15": helpers.HELP_15, "hb16": helpers.HELP_16
    }

    if cb in help_dict:
        await CallbackQuery.edit_message_text(help_dict[cb], reply_markup=keyboard)

Dil_Text = ("ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\n"
            "ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ <a href={0}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a>\n\n"
            "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: <code>/</code>")

@app.on_callback_query(filters.regex("next_page") & ~BANNED_USERS)
@languageCB
async def next_page(client, CallbackQuery, _):
    menu_next = second_page(_)
    await CallbackQuery.message.edit_text(Dil_Text.format(SUPPORT_CHAT), reply_markup=menu_next)

@app.on_callback_query(filters.regex("prev_page") & ~BANNED_USERS)
@languageCB
async def prev_page(client, CallbackQuery, _):
    menu_back = first_page(_)
    await CallbackQuery.message.edit_text(Dil_Text.format(SUPPORT_CHAT), reply_markup=menu_back)
