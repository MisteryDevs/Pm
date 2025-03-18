from pyrogram import Client, filters
from pyrogram.types import Message
import qrcode
from SONALI import app
from PIL import Image
import io


# Function to create a QR code
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")  # Background white, text black

    # Save the QR code to a bytes object to send with Pyrogram
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)  # Reset buffer position

    return img_bytes


@app.on_message(filters.command("qr"))
def qr_handler(client: Client, message: Message):
    # Extracting text after /qr command
    command_text = message.text.split(" ", 1)
    
    if len(command_text) > 1:
        input_text = command_text[1]  # Getting the text after the command
        qr_image = generate_qr_code(input_text)
        
        message.reply_photo(qr_image, caption="Here's your QR Code ✅")
    else:
        message.reply_text("❍ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛᴇxᴛ ғᴏʀ ᴛʜᴇ Qʀ ᴄᴏᴅᴇ. \n\n**Example:** `/qr Hello World`")
