from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from SONALI import app

def help_pannel(_, START: Union[bool, int] = None, page: int = 1):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")]
    mark = second if START else first

    buttons = [
        [_["H_B_1"], _["H_B_2"], _["H_B_3"]],
        [_["H_B_4"], _["H_B_5"], _["H_B_6"]],
        [_["H_B_7"], _["H_B_8"], _["H_B_9"]],
        [_["H_B_10"], _["H_B_11"], _["H_B_12"]],
        [_["H_B_13"], _["H_B_14"], _["H_B_15"]],
        [_["H_B_16"], _["H_B_17"], _["H_B_18"]],
        [_["H_B_19"], _["H_B_20"], _["H_B_21"]],
        [_["H_B_22"], _["H_B_23"], _["H_B_24"]],
        [_["H_B_25"], _["H_B_26"], _["H_B_27"]],
    ]

    # Page-based slicing
    start_index = (page - 1) * 3
    end_index = start_index + 3
    current_buttons = [
        [InlineKeyboardButton(text=text, callback_data=f"help_callback hb{start_index + i + 1}")]
        for i, text in enumerate(sum(buttons[start_index:end_index], []))
    ]

    # Navigation Buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Previous", callback_data=f"help_page {page - 1}"))
    if page < 3:
        nav_buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"help_page {page + 1}"))

    if nav_buttons:
        current_buttons.append(nav_buttons)

    current_buttons.append(mark)

    return InlineKeyboardMarkup(current_buttons)


# ✅ Callback Handler to Update Pages
@app.on_callback_query(filters.regex(r"help_page (\d+)"))
async def help_page_callback(client: Client, query):
    page = int(query.matches[0].group(1))
    await query.message.edit_reply_markup(reply_markup=help_pannel(_, page=page))


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")]]
    )


def private_help_panel(_):
    return [
        [InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help")],
    ]
