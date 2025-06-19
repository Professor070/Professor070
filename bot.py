import os
import json
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN
image = 'photo_2025-06-19_18-26-58.jpg'

# ─── Logging Configuration ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ─── Paths and Constants ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTION_STORE = os.path.join(BASE_DIR, "caption_store.json")

# ─── Fancy Unicode Map ─────────────────────────────────────────────────
fancy_map = {
    "A": "𝐀", "B": "𝐁", "C": "𝐂", "D": "𝐃", "E": "𝐄", "F": "𝐅", "G": "𝐆", "H": "𝐇", "I": "𝐈", "J": "𝐉", "K": "𝐊", "L": "𝐋", "M": "𝐌", "N": "𝐍", "O": "𝐎", "P": "𝐏", "Q": "𝐐", "R": "𝐑", "S": "𝐒", "T": "𝐓", "U": "𝐔", "V": "𝐕", "W": "𝐖", "X": "𝐗", "Y": "𝐘", "Z": "𝐙",
    "a": "𝐚", "b": "𝐛", "c": "𝐜", "d": "𝐝", "e": "𝐞", "f": "𝐟", "g": "𝐠", "h": "𝐡", "i": "𝐢", "j": "𝐣", "k": "𝐤", "l": "𝐥", "m": "𝐦", "n": "𝐧", "o": "𝐨", "p": "𝐩", "q": "𝐪", "r": "𝐫", "s": "𝐬", "t": "𝐭", "u": "𝐮", "v": "𝐯", "w": "𝐰", "x": "𝐱", "y": "𝐲", "z": "𝐳",
    "0": "𝟎", "1": "𝟏", "2": "𝟐", "3": "𝟑", "4": "𝟒", "5": "𝟓", "6": "𝟔", "7": "𝟕", "8": "𝟖", "9": "𝟗",
    ".": ".", "_": "_", " ": " ", "-": "-", "(": "(", ")": ")", "[": "[", "]": "]"
}

def to_fancy(text):
    return "".join(fancy_map.get(c, c) for c in text)

# ─── Load/Save Captions ────────────────────────────────────────────────
def load_captions():
    try:
        with open(CAPTION_STORE, "r", encoding="utf-8") as f:
            logger.info("✅ Caption store loaded.")
            return json.load(f)
    except FileNotFoundError:
        logger.warning("⚠️ Caption store not found, creating a new one.")
        return {}
    except Exception as e:
        logger.error(f"❌ Failed to load caption store: {e}")
        return {}

def save_captions(captions):
    try:
        with open(CAPTION_STORE, "w", encoding="utf-8") as f:
            json.dump(captions, f, ensure_ascii=False, indent=2)
        logger.info("✅ Captions saved.")
    except Exception as e:
        logger.error(f"❌ Failed to save captions: {e}")

captions = load_captions()

# ─── Pyrogram Bot Setup ────────────────────────────────────────────────
app = Client("autocaption_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("setcaption") & filters.channel)
async def set_caption(client, message: Message):
    channel_id = str(message.chat.id)
    if len(message.command) > 1:
        caption = message.text.split(" ", 1)[1]
        captions[channel_id] = caption
        save_captions(captions)
        await message.reply(
            "<b>✨ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐂𝐚𝐩𝐭𝐢𝐨𝐧 𝐒𝐚𝐯𝐞𝐝! ✨</b>\n\n"
            "<b>📝 𝐘𝐨𝐮𝐫 𝐧𝐞𝐰 𝐜𝐚𝐩𝐭𝐢𝐨𝐧:</b>\n"
            f"<code>{caption}</code>\n\n"
            "<b>🔧 𝐓𝐢𝐩:</b>\n"
            "<pre>Use {filename} in your caption to automatically insert the video file name in a stylish Unicode font! 🎬✨</pre>"
        )
        logger.info(f"📌 Caption set for channel {channel_id}")
    else:
        await message.reply(
            "⚠️ Usage: /setcaption [your caption here]\n"
            "You can use {filename} in your caption to insert the video filename. Example:\n"
            "/setcaption ✨ 𝐓𝐢𝐭𝐥𝐞 :- \"{filename}\""
        )
        logger.warning("⚠️ setcaption used without text.")

@app.on_message(filters.video & filters.channel)
def auto_caption(client, message: Message):
    video = message.video
    raw_title = video.file_name if video and video.file_name else "Unknown Title"
    fancy_title = to_fancy(raw_title)
    channel_id = str(message.chat.id)
    custom_caption = captions.get(channel_id)

    if custom_caption:
        caption = custom_caption.replace("{filename}", fancy_title).replace("{{filename}}", fancy_title)
    else:
        caption = f'✨ 𝐓𝐢𝐭𝐥𝐞 :- "{fancy_title}"'

    try:
        client.edit_message_caption(message.chat.id, message.id, caption)
        logger.info(f"✏️ Caption added to video: {raw_title}")
    except Exception as e:
        logger.error(f"❌ Failed to edit caption: {e}")

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_photo(
        photo=image,
        caption=(
            "✨ <b>𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐀𝐮𝐭𝐨 𝐂𝐚𝐩𝐭𝐢𝐨𝐧 𝐁𝐨𝐭! ✨</b>\n\n"
            "🎬 <b>Instantly add stylish Unicode captions to your channel videos!</b>\n\n"
            "📌 <b>How to set your custom caption:</b>\n"
            "/setcaption ✨ 𝐓𝐢𝐭𝐥𝐞 :- <code>\"{filename}\"</code>\n\n"
            "💡 <b>Tip:</b> Use <code>{filename}</code> anywhere in your caption to insert the video file name automatically, beautifully styled in Unicode!\n\n"
            "🚀 <i>Simple, fast, and elegant!</i>"
        )
    )
    logger.info(f"🚀 Bot started by user {message.from_user.id}")

if __name__ == "__main__":
    logger.info("🤖 Bot is starting...")
    app.run()
