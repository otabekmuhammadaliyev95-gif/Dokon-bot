import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("8827197387:AAEA_gSbAWl6BCPLO3k4F1NVcL911C2cSX8")
ADMIN_USERNAME = "@Muhammadaliyev9"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

mahsulotlar = [
    {"nomi": "Mahsulot 1", "narxi": "50,000 so'm"},
    {"nomi": "Mahsulot 2", "narxi": "80,000 so'm"},
    {"nomi": "Mahsulot 3", "narxi": "120,000 so'm"},
]

def asosiy_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Mahsulotlar")],
            [KeyboardButton(text="🛒 Buyurtma berish")],
            [KeyboardButton(text="📞 Bog'lanish")],
        ],
        resize_keyboard=True
    )
    return kb

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Do'konimizga xush kelibsiz 🛍\nQuyidagi menyudan tanlang:",
        reply_markup=asosiy_menu()
    )

@dp.message(lambda m: m.text == "📦 Mahsulotlar")
async def mahsulotlar_royxati(message: types.Message):
    matn = "📦 *Mahsulotlarimiz:*\n\n"
    for i, m in enumerate(mahsulotlar, 1):
        matn += f"{i}. {m['nomi']} — {m['narxi']}\n"
    await message.answer(matn, parse_mode="Markdown")

@dp.message(lambda m: m.text == "🛒 Buyurtma berish")
async def buyurtma(message: types.Message):
    await message.answer(
        "Buyurtma berish uchun quyidagi formatda yozing:\n\n"
        "📝 *Ism: ...*\n"
        "📱 *Telefon: ...*\n"
        "📦 *Mahsulot: ...*",
        parse_mode="Markdown"
    )

@dp.message(lambda m: m.text == "📞 Bog'lanish")
async def boglanish(message: types.Message):
    await message.answer(
        f"📞 Admin bilan bog'lanish:\n{ADMIN_USERNAME}\n\nIsh vaqti: 9:00 — 18:00"
    )

@dp.message()
async def buyurtma_qabul(message: types.Message):
    if any(x in message.text.lower() for x in ["ism:", "telefon:", "mahsulot:"]):
        await message.answer("✅ Buyurtmangiz qabul qilindi!\nTez orada admin siz bilan bog'lanadi.")
    else:
        await message.answer("Iltimos, menyudan foydalaning 👇", reply_markup=asosiy_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())
