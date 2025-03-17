# Importing important modules & bot
from SONALI import app
from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Creating first partition of menu
def first_page(_):
	controll_button = [
	    InlineKeyboardButton(text="◁", callback_data="help_prev"), 
	    InlineKeyboardButton(text="HOME", callback_data="settings_back_helper"), 
	    InlineKeyboardButton(text="▷", callback_data="help_next")  # Fixed next button
	]
	first_page_menu = InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"), InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"), InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3")],
			[InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"), InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"), InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6")],
			[InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"), InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"), InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9")],
			[InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"), InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"), InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12")],
			controll_button,
		]
	)
	return first_page_menu

# Creating second partition of menu
def second_page(_):
	controll_button = [
	    InlineKeyboardButton(text="◁", callback_data="help_prev"),  # Fixed previous button
	    InlineKeyboardButton(text="HOME", callback_data="settings_back_helper"), 
	    InlineKeyboardButton(text="▷", callback_data="help_next")  # Fixed next button
	]
	second_page_menu = InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"), InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"), InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15")],
			[InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16"), InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17"), InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18")],
			[InlineKeyboardButton(text=_["H_B_19"], callback_data="help_callback hb19")],
			[InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20"), InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21"), InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22")],
			[InlineKeyboardButton(text=_["H_B_23"], callback_data="help_callback hb23"), InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24"), InlineKeyboardButton(text=_["H_B_25"], callback_data="help_callback hb25")],
			controll_button,
		]
	)
	return second_page_menu

# Common back button
def help_back_markup(_):
	return InlineKeyboardMarkup([[InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")]])

# Ease of access
def private_help_panel(_):
	return [[InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help")]]
