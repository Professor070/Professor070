import os
import re
import logging
import asyncio
import requests
import json
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 29388606
API_HASH = "ddc1032e4e1fd0216362d18b68afd848"
BOT_TOKEN = "7233882118:AAFbD-DrSzfoetbbzN7vWjomOcWWEr5N0d0"

GREETING_IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "greeting.jpg")

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def expand_pin_it_url(url):
    try:
        logger.info(f"Expanding shortlink: {url}")
        r = requests.head(url, allow_redirects=True, timeout=10)
        long_url = r.url
        logger.info(f"Expanded to: {long_url}")
        return long_url
    except Exception as e:
        logger.error(f"Failed to expand {url}: {e}")
        return url

def normalize_pin_url(url):
    m = re.search(r"(https://www\.pinterest\.com/pin/\d+)", url)
    if m:
        return m.group(1) + "/"
    return url

def extract_pinterest_video(pin_url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    try:
        r = requests.get(pin_url, headers=headers, timeout=20)
        r.raise_for_status()
    except Exception as e:
        logger.error(f"Error fetching Pinterest URL: {e}")
        return None, f"❌ Could not access the link ({str(e)}). Is it public and correct?"

    text = r.text

    try:
        script_match = re.search(r'<script id="__PWS_DATA__" type="application/json">(.+?)</script>', text)
        if script_match:
            data = json.loads(script_match.group(1))
            pins = data.get("props", {}).get("initialReduxState", {}).get("pins", {})
            for pinid, pindata in pins.items():
                if "videos" in pindata:
                    video_list = pindata["videos"].get("video_list", {})
                    mp4s = [v["url"] for v in video_list.values() if v.get("url")]
                    if mp4s:
                        return mp4s, None
    except Exception as e:
        logger.warning(f"Failed to parse __PWS_DATA__ json: {e}")

    videos = re.findall(r'"contentUrl":"(https:[^"]+\.mp4)"', text)
    if videos:
        return videos, None

    return None, (
        "❌ Only Pinterest video pins are supported.\n"
        "For images or carousels, please use the Pinterest app or website to save them."
    )

app = Client("pinterest_media_saver_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    greeting_text = (
        "🎬 Welcome to Pinterest Video Downloader!\n\n"
        "🚩 What can I do?\n"
        "➤ Download Pinterest Video Pins instantly.\n"
        "➤ Just send me any Pinterest video pin link (pinterest.com or pin.it short links) and I'll fetch the video for you.\n\n"
        "⚠️ Note: Images and carousels are NOT supported. Please use the Pinterest app/website for those.\n\n"
        "🚀 Fast • Secure • Easy\n"
        "Share me with your friends if you find this useful!"
    )
    if os.path.exists(GREETING_IMAGE):
        await message.reply_photo(
            photo=GREETING_IMAGE,
            caption=greeting_text
        )
    else:
        await message.reply(
            greeting_text
        )
    logger.info(f"🚀 Bot started by user {getattr(message.from_user, 'id', None)}")

@app.on_message(filters.text)
async def handle_pinterest(client, message: Message):
    text = message.text.strip()
    if "pinterest." not in text and "pin.it" not in text:
        return

    logger.info(f"Received link: {text}")

    url_match = re.search(r'(https?://[^\s]+)', text)
    if not url_match:
        await message.reply("❌ No link found in your message.")
        logger.warning("No link found in message.")
        return

    url = url_match.group(1)

    if "pin.it" in url:
        url = expand_pin_it_url(url)
        logger.info(f"Shortlink expanded to: {url}")

    url = normalize_pin_url(url)
    logger.info(f"Normalized url: {url}")

    status_msg = await message.reply("⏳ Processing your Pinterest video link...")

    videos, error_msg = extract_pinterest_video(url)
    if error_msg:
        await status_msg.edit(error_msg)
        logger.info(f"Video extract error: {error_msg}")
        return
    if not videos:
        await status_msg.edit("❌ No video found or unsupported pin type.")
        logger.info("No video found.")
        return

    sent = False
    for vurl in videos:
        try:
            video_msg = await client.send_video(message.chat.id, vurl)
            # Send done message after the video (as a reply)
            done_text = (
                "✅ Here is your Pinterest Video!\n\n"
                "😊 Thank you for using Pinterest Video Downloader!\n"
                "If you found this useful, share with your friends 🎉"
            )
            await client.send_message(
                chat_id=message.chat.id,
                text=done_text,
                reply_to_message_id=video_msg.id
            )
            sent = True
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.warning(f"Failed sending video: {e}")
    if sent:
        await status_msg.delete()
        logger.info("Video sent and done message delivered.")
    else:
        await status_msg.edit("❌ Video extraction succeeded, but failed to send video (bad URL or Telegram error).")
        logger.warning("Failed to send any video.")

if __name__ == "__main__":
    logger.info("🤖 Pinterest Telegram Bot is starting...")
    app.run()
