import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

# TELEGRAM BOT TOKENINGIZ
TELEGRAM_TOKEN = "8577469434:AAEthC-N65LotFay--HEpw0d6Pm5HMTrmoY"

# BEPUL GEMINI AI KALITI
GEMINI_API_KEY = "AIzaSyD-ExampleKey-DoNotChangeIfWorking" 

# Sun'iy intellekt xarakteri
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Siz erkin, mustaqil va juda aqlli AI agentsiz. Ismingiz - Rajabali AI. Foydalanuvchiga har qanday qiyin vazifalarni yechishda, kod yozishda yoki shunchaki suhbatlashishda yordam bering va doim o'zbek tilida chiroyli javob qaytaring."
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}!\n\n"
        "Men **Rajabali AI** erkin sun'iy intellekt agentiman. Menga istalgan savolingizni berishingiz mumkin! 🚀"
    )

@dp.message()
async def ai_chat_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = model.generate_content(message.text)
        await message.reply(response.text, parse_mode="Markdown")
    except Exception as e:
        await message.reply("Hozircha xabaringizni qayta ishlay olmayapman. Birozdan so'ng qayta urinib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
