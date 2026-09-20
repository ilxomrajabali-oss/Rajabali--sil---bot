import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai
from aiohttp import web

# TO'G'RI TELEGRAM BOT TOKENINGIZ
TELEGRAM_TOKEN = "8577469434:AAEthC-N65LotFay--HEpw0d6Pm5HMTrmoY"

# GOOGLE AI STUDIODAN OLGAN YANGI SHAXSIY KALITINGIZ
GEMINI_API_KEY = "Ab8RN6KAvhdxWWWpEKP91Mw-D4d2j0btL7zdJqKe2YxuMRclLQ"

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
genai.configure()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Siz erkin, mustaqil va juda aqlli AI agentsiz. Ismingiz - Rajabali AI. Foydalanuvchiga har qanday qiyin vazifalarni yechishda yordam bering va doim o'zbek tilida chiroyli javob qaytaring."
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.first_name}!\n\nMen **Rajabali AI** erkin sun'iy intellekt agentiman. Menga istalgan savolingizni yozishingiz mumkin! 🚀")

@dp.message()
async def ai_chat_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = model.generate_content(message.text)
        await message.reply(response.text, parse_mode="Markdown")
    except Exception as e:
        await message.reply("Xabaringizni qayta ishlashda tizim xatosi bo'ldi. Birozdan so'ng qayta urinib ko'ring.")

async def handle(request):
    return web.Response(text="Bot is active!")

async def main():
    # Telegramdagi barcha eski qolib ketgan noto'g'ri so'rovlarni majburlab o'chirish (Conflict'ni davolash)
    await bot.delete_webhook(drop_pending_updates=True)
    
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    await asyncio.gather(
        site.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
