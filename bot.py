import re
import asyncio
import os
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def parse_time(time_str):
    match = re.fullmatch(r"(\d+)([mhd])", time_str.lower())
    if not match:
        return None
    value, unit = match.groups()
    value = int(value)
    if unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 60 * 60
    elif unit == 'd':
        return value * 60 * 60 * 24
    return None

@client.on(events.NewMessage(pattern='/adduser'))
async def add_user(event):
    parts = event.message.text.strip().split()
    if len(parts) != 3:
        await event.reply("❗ Format: /adduser <user_id> <time>\nযেমন: /adduser 123456789 30m / 12h / 7d")
        return

    try:
        user_id = int(parts[1])
        time_input = parts[2]
        seconds = parse_time(time_input)

        if seconds is None:
            await event.reply("❗ Invalid time format. Use <number><m/h/d>. উদাহরণ: 30m, 12h, 7d")
            return

        chat_id = event.chat_id
        await event.reply(f"✅ User {user_id} will be removed after {time_input}.")

        await asyncio.sleep(seconds)

        user = await client.get_entity(user_id)
        await client.kick_participant(chat_id, user)
        await client.send_message(user_id, "❗ আপনার সাবস্ক্রিপশন শেষ হয়ে গেছে। পুনরায় সাবস্ক্রাইব করতে ইনবক্স করুন 👉 @dudh_cha_admin\n📢 ধন্যবাদ আমাদের সাথে থাকার জন্য!")
        await event.reply(f"🚫 User {user_id} removed.")

    except Exception as e:
        await event.reply(f"⚠️ Error: {e}")

@client.on(events.NewMessage(pattern='/id'))
async def get_id(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()
        await event.reply(f"👤 Name: {user.first_name or 'N/A'}\n🔹 Username: @{user.username or 'N/A'}\n🆔 User ID: {user.id}")
    else:
        await event.reply("❗ প্রথমে কারো মেসেজে রিপ্লাই করে /id লিখো।")

client.start()
client.run_until_disconnected()
