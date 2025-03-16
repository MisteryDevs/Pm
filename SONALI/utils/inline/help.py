from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from SONALI import app

def help_pannel(_, page: int = 1):
    all_buttons = [
        # Page 1 (hb1 - hb9)
        [
            InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
            InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
            InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
        ],
        [
            InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
            InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
            InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
        ],
        [
            InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
            InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
            InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9"),
        ],
        # Page 2 (hb10 - hb18)
        [
            InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"),
            InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"),
            InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12"),
        ],
        [
            InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"),
            InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"),
            InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15"),
        ],
        [
            InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16"),
            InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17"),
            InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18"),
        ],
        # Page 3 (hb19 - hb27)
        [
            InlineKeyboardButton(text=_["H_B_19"], callback_data="help_callback hb19"),
            InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20"),
            InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21"),
        ],
        [
            InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22"),
            InlineKeyboardButton(text=_["H_B_23"], callback_data="help_callback hb23"),
            InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24"),
        ],
        [
            InlineKeyboardButton(text=_["H_B_25"], callback_data="help_callback hb25"),
            InlineKeyboardButton(text=_["H_B_26"], callback_data="help_callback hb26"),
            InlineKeyboardButton(text=_["H_B_27"], callback_data="help_callback hb27"),
        ],
    ]

    # Selecting buttons for the current page (each page has 3 rows)
    start_idx = (page - 1) * 3
    end_idx = start_idx + 3
    selected_buttons = all_buttons[start_idx:end_idx]

    # Navigation Buttons (⬅ Back, 🏠 Home, ➡ Next)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Back", callback_data=f"help_page_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(text="🏠 Home", callback_data="help_home"))
    if page < 3:
        nav_buttons.append(InlineKeyboardButton(text="➡ Next", callback_data=f"help_page_{page+1}"))

    # Adding navigation row
    selected_buttons.append(nav_buttons)

    return InlineKeyboardMarkup(selected_buttons)
