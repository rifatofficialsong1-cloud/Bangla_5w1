import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# রেন্ডারে সচল রাখার জন্য ছোট ওয়েব সার্ভার
web = Flask('')

@web.route('/')
def home():
    return "Bot is Running!"

def run():
    web.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# এনভায়রনমেন্ট ভ্যারিয়েবল
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SMART_LINK = os.environ.get("SMART_LINK")

app = Client("video_lock_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_callback_query()
async def handle_unlock(client, callback_query):
    data = callback_query.data
    if data.startswith("verify_"):
        video_id = data.split("_")[1]
        await callback_query.message.edit_text(
            "⚠️ ভিডিওটি লক করা আছে!\n\nঅ্যাড দেখে আনলক করুন:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Watch Ad", url=SMART_LINK)],
                [InlineKeyboardButton("✅ I have Watched", callback_query_data=f"unlock_{video_id}")]
            ])
        )
    elif data.startswith("unlock_"):
        video_id = data.split("_")[1]
        await client.send_video(chat_id=callback_query.message.chat.id, video=video_id)

@app.on_message(filters.video & filters.private)
async def get_video(client, message):
    file_id = message.video.file_id
    await message.reply(f"আপনার ভিডিও বাটন লিংক:\n\n`https://t.me/{app.me.username}?start={file_id}`")

if __name__ == "__main__":
    keep_alive() # ওয়েব সার্ভার স্টার্ট
    app.run() # বট স্টার্ট
