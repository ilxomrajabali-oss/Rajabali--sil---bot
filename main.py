import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai
from aiohttp import web

# TO'G'RI BOT TOKENI (BotFather'dan olingan oxirgi tokenni tekshirib qo'ying)
TELEGRAM_TOKEN ="8577469434:AAEthC-N65LotFay--HEpwOd6Pm5HMTrmoY"


# BEPUL GEMINI AI KALITI
GEMINI_API_KEY = "Ab8RN6KAvhdxWWWpEKP91Mw-D4d2j0btL7zdJqKe2YxuMRclLQ"

# Sun'iy intellekt xarakteri
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Siz erkin, mustaqil va juda aqlli AI agentsiz. Ismingiz - Rajabali AI. Foydalanuvchiga har qanday qiyin vazifalarni yechishda yordam bering va doim o'zbek tilida chiroyli javob qaytaring."
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.first_name}!\n\nMen **Rajabali AI** erkin sun'iy intellekt agentiman. Menga yozishingiz mumkin! 🚀")

@dp.message()
async def ai_chat_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = model.generate_content(message.text)
        await message.reply(response.text, parse_mode="Markdown")
    except Exception as e:
        await message.reply("Hozircha xabaringizni qayta ishlay olmayapman. Birozdan so'ng qayta urinib ko'ring.")

# Render'da port muammosini yechish uchun kichik veb-server
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    # Render beradigan portni olish (agar bo'lmasa 10000)
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    # Veb-server va Telegram botni bir vaqtda ishga tushirish
    await asyncio.gather(
        site.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())

  
