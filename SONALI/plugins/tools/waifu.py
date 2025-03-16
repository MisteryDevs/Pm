from pyrogram import Client, filters
import aiohttp
from SONALI import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# VIP Inline Button  
EVAA = [
    [
        InlineKeyboardButton(text="➕ 𝐀𝐃𝐃 𝐌𝐄 𝐁𝐀𝐁𝐘 💖", url="https://t.me/Sweety_music09_BOT?startgroup=true"),
    ],
]

waifu_api_url = 'https://api.waifu.im/search'


async def get_waifu_data(tags):
    """ Fetch waifu image from API asynchronously """
    params = {
        'included_tags': tags,
        'height': '>=2000'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(waifu_api_url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return None


@app.on_message(filters.command("waifu"))
async def waifu_command(client, message):
    try:
        args = message.text.split(maxsplit=1)
        tags = [args[1]] if len(args) > 1 else ['maid']  # Default is 'maid' if no tag given

        waifu_data = await get_waifu_data(tags)

        if waifu_data and 'images' in waifu_data and waifu_data['images']:
            first_image = waifu_data['images'][0]
            image_url = first_image['url']

            await message.reply_photo(
                image_url,
                caption=(
                    "✨ 𝐇𝐞𝐫𝐞'𝐬 𝐘𝐨𝐮𝐫 𝐏𝐞𝐫𝐟𝐞𝐜𝐭 𝐖𝐚𝐢𝐟𝐮! 💖\n"
                    f"📌 𝐂ᴀᴛᴇɢᴏʀʏ: `{tags[0].capitalize()}`\n"
                    "🔗 Ꮲᴏᴡᴇʀᴇᴅ 𝐁ʏ: [•⏤‌𝄞⃝🍧 ‌⃪‌𝐒ᴡᴇᴇᴛʏ 𝐌ᴜsɪᴄ♥️꯭꯭꯭꯭ ꯭꯭᪳𝆺𝅥"
                ),
                reply_markup=InlineKeyboardMarkup(EVAA),
            )
        else:
            await message.reply_text("❌ No waifu found in this category! Try another tag.")

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`")
