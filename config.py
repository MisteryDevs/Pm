import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", "14050586"))  # Default value added
API_HASH = getenv("API_HASH", "42a60d9c657b106370c79bb0a8ac560c")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "your_bot_token")

# Get your bot username from @BotFather
BOT_USERNAME = getenv("BOT_USERNAME", "Rishu")  # FIXED

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "10000"))  # Default value added

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", "-1001992970818"))  # Fixed None issue

OWNER_ID = int(getenv("OWNER_ID", "5738579437"))  # Fixed None issue


# Heroku deployment settings
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None) or "my_default_app"
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None) or "your_default_api_key"

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/MisteryDevs/Pm")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)  # Only required if repo is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Ur_Rishu_143")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Ur_Support07")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", "False"))

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))  # 100 MB
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824"))  # 1 GB

# Get your pyrogram v2 session from @king_string_session_bot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/cteuxa.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/dmx463.jpg")
PLAYLIST_IMG_URL = "https://files.catbox.moe/bizazk.jpg"
STATS_IMG_URL = "https://files.catbox.moe/xbfjiz.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/8e3552aa743ffdb6f18c9.jpg"
TELEGRAM_VIDEO_URL = "https://i.ibb.co/39WSm9zM/IMG-20250207-080405-192.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/rmt6yk.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/63go4k.jpg"
YOUTUBE_IMG_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL URL is wrong. Ensure it starts with https://")

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit("[ERROR] - Your SUPPORT_CHAT URL is wrong. Ensure it starts with https://")
