from SONALI import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

#------------------------------------------------------------------------#

# Creating first partition of menu
def first_page(_):
    controll_button = [InlineKeyboardButton(text="◁", callback_data="fourth_page"), 
                       InlineKeyboardButton(text="HOME", callback_data="settingsback_helper"), 
                       InlineKeyboardButton(text="▷", callback_data="second_page")]
    first_page_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"), InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"), InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3")],
            [InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"), InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"), InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6")],
            [InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"), InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"), InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9")],
            controll_button,
        ]
    )
    return first_page_menu

# Creating second partition of menu
def second_page(_):
    controll_button = [InlineKeyboardButton(text="◁", callback_data="first_page"), 
                       InlineKeyboardButton(text="HOME", callback_data="settingsback_helper"), 
                       InlineKeyboardButton(text="▷", callback_data="third_page")]
    second_page_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"), InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"), InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12")],
            [InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"), InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"), InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15")],
            [InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16"), InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17"), InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18")],
            controll_button,
        ]
    )
    return second_page_menu

# Creating third partition of menu
def third_page(_):
    controll_button = [InlineKeyboardButton(text="◁", callback_data="second_page"), 
                       InlineKeyboardButton(text="HOME", callback_data="settingsback_helper"), 
                       InlineKeyboardButton(text="▷", callback_data="fourth_page")]
    third_page_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=_["H_B_19"], callback_data="help_callback hb19"), InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20"), InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21")],
            [InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22"), InlineKeyboardButton(text=_["H_B_23"], callback_data="help_callback hb23"), InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24")],
            [InlineKeyboardButton(text=_["H_B_25"], callback_data="help_callback hb25"), InlineKeyboardButton(text=_["H_B_26"], callback_data="help_callback hb26"), InlineKeyboardButton(text=_["H_B_27"], callback_data="help_callback hb27")],
            controll_button,
        ]
    )
    return third_page_menu

# Creating fourth partition of menu
def fourth_page(_):
    controll_button = [InlineKeyboardButton(text="◁", callback_data="third_page"), 
                       InlineKeyboardButton(text="HOME", callback_data="settingsback_helper"), 
                       InlineKeyboardButton(text="▷", callback_data="first_page")]
    fourth_page_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=_["H_B_28"], callback_data="help_callback hb28"), InlineKeyboardButton(text=_["H_B_29"], callback_data="help_callback hb29"), InlineKeyboardButton(text=_["H_B_30"], callback_data="help_callback hb30")],
            [InlineKeyboardButton(text=_["H_B_31"], callback_data="help_callback hb31"), InlineKeyboardButton(text=_["H_B_32"], callback_data="help_callback hb32"), InlineKeyboardButton(text=_["H_B_33"], callback_data="help_callback hb33")],
            [InlineKeyboardButton(text=_["H_B_34"], callback_data="help_callback hb34"), InlineKeyboardButton(text=_["H_B_35"], callback_data="help_callback hb35"), InlineKeyboardButton(text=_["H_B_36"], callback_data="help_callback hb36")],
            controll_button,
        ]
    )
    return fourth_page_menu

# Handling Callback Queries
@app.on_callback_query(filters.regex("first_page"))
async def show_first_page(client, query: CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=first_page(_))

@app.on_callback_query(filters.regex("second_page"))
async def show_second_page(client, query: CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=second_page(_))

@app.on_callback_query(filters.regex("third_page"))
async def show_third_page(client, query: CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=third_page(_))

@app.on_callback_query(filters.regex("fourth_page"))
async def show_fourth_page(client, query: CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=fourth_page(_))

# Common back button
def help_back_markup(_):
    upl = InlineKeyboardMarkup([[InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")]])
    return upl

# Ease of access
def private_help_panel(_):
    buttons = [[InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help")]]
    return buttons
