import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@Muhammadaliyev9"

bot = Bot(token="8827197387:AAEA_gSbAWl6BCPLO3k4F1NVcL911C2cSX8")
dp = Dispatcher(bot)

mahsulotlar = [
    {"nomi": "Mahsulot 1", "narxi": "50,000 so'm"},
    {"nomi": "Mahsulot 2", "narxi": "80,000 so'm"},
    {"nomi": "Mahsulot 3", "narxi": "120,000 so'm"},
]

def asosiy_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📦 Mahsulotlar"))
    kb.add(KeyboardButton("🛒 Buyurtma berish"))
    kb.add(KeyboardButton("📞 Bog'lanish"))
    return kb

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Do'konimizga xush kelibsiz 🛍\nQuyidagi menyudan tanlang:",
        reply_markup=asosiy_menu()
    )

@dp.message_handler(lambda m: m.text == "📦 Mahsulotlar")
async def mahsulotlar_royxati(message: types.Message):
    matn = "📦 *Mahsulotlarimiz:*\n\n"
    for i, m in enumerate(mahsulotlar, 1):
        matn += f"{i}. {m['nomi']} — {m['narxi']}\n"
    await message.answer(matn, parse_mode="Markdown")

@dp.message_handler(lambda m: m.text == "🛒 Buyurtma berish")
async def buyurtma(message: types.Message):
    await message.answer(
        "Buyurtma berish uchun quyidagi formatda yozing:\n\n"
        "📝 *Ism: ...*\n"
        "📱 *Telefon: ...*\n"
        "📦 *Mahsulot: ...*",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda m: m.text == "📞 Bog'lanish")
async def boglanish(message: types.Message):
    await message.answer(
        f"📞 Admin bilan bog'lanish:\n{ADMIN_USERNAME}\n\nIsh vaqti: 9:00 — 18:00"
    )

@dp.message_handler()
async def buyurtma_qabul(message: types.Message):
    if any(x in message.text.lower() for x in ["ism:", "telefon:", "mahsulot:"]):
        await message.answer("✅ Buyurtmangiz qabul qilindi!\nTez orada admin siz bilan bog'lanadi.")
    else:
        await message.answer("Iltimos, menyudan foydalaning 👇", reply_markup=asosiy_menu())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
if __name__ == "__main__":
    asyncio.run(main())
