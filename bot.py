import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার API ID, Hash এবং Bot Token এখানে দিন (অথবা Render Environment এ সেট করুন)
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"
SMART_LINK = "YOUR_ADSTERRA_SMART_LINK"

app = Client("video_lock_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ভিডিও হ্যান্ডলার (যখন ইউজার বাটনে ক্লিক করবে)
@app.on_callback_query()
async def handle_unlock(client, callback_query):
    data = callback_query.data
    
    if data.startswith("verify_"):
        video_id = data.split("_")[1]
        
        # ইউজারকে অ্যাডের লিংকে পাঠানো
        await callback_query.message.edit_text(
            "⚠️ ভিডিওটি লক করা আছে!\n\nনিচের লিংকে ক্লিক করে অ্যাডটি দেখুন, তারপর 'Check' বাটনে ক্লিক করুন।",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Watch Ad to Unlock", url=SMART_LINK)],
                [InlineKeyboardButton("✅ I have Watched", callback_query_data=f"unlock_{video_id}")]
            ])
        )

    elif data.startswith("unlock_"):
        video_id = data.split("_")[1]
        # এখানে আসলে ভিডিওটি ইউজারকে পাঠিয়ে দেওয়া হবে
        # নোট: এখানে ভিডিওর File ID ব্যবহার করা হচ্ছে
        await callback_query.message.delete()
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=video_id,
            caption="✅ আপনার ভিডিওটি আনলক হয়েছে! উপভোগ করুন।"
        )

# এডমিন যখন ভিডিও পাঠাবে চ্যানেলে পোস্ট করার জন্য
@app.on_message(filters.video & filters.me)
async def post_video(client, message):
    file_id = message.video.file_id
    await client.send_message(
        chat_id="YOUR_CHANNEL_ID", # আপনার চ্যানেলের ইউজারনেম বা আইডি
        text="🎬 একটি নতুন ভিডিও আপলোড করা হয়েছে!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Watch Video", callback_query_data=f"verify_{file_id}")]
        ])
    )

app.run()
