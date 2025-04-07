import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

# Lấy các biến môi trường
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
AUTHORIZED_USERS = os.getenv('AUTHORIZED_USERS', '').split(',')

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

# Khởi tạo bot và dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Khởi tạo OpenAI
openai.api_key = OPENAI_API_KEY

# Hàm xử lý tin nhắn
@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in AUTHORIZED_USERS:
        await message.reply("Bạn không có quyền sử dụng bot này.")
        return

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message['content'].strip()
        await message.reply(reply)
    except Exception as e:
        logging.error(f"Lỗi khi gọi OpenAI: {e}")
        await message.reply("Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
