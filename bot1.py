import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# === TOKEN ===
BOT_TOKEN = "BU_YERGA_TOKENINGIZNI_QOYING"
ADMIN_USERNAME = "@sizning_username"  # admin username

bot = Bot(token="8827197387:AAE7sJsUxHwvLqN_JoYR737yXEUoe5PQ5Mc")
dp = Dispatcher()

# === MAHSULOTLAR ===
mahsulotlar = [
    {"nomi": "SHokolad", "narxi": "50,000 so'm"},
    {"nomi": "Oyinchoq mashina", "narxi": "80,000 so'm"},
    {"nomi": "Oyinchoqlar toplami", "narxi": "120,000 so'm"},
]

# === KLAVIATURA ===
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

# === /start ===
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Do'konimizga xush kelibsiz 🛍\n"
        "Quyidagi menyudan tanlang:",
        reply_markup=asosiy_menu()
    )

# === MAHSULOTLAR ===
@dp.message(lambda m: m.text == "📦 Mahsulotlar")
async def mahsulotlar_royxati(message: types.Message):
    matn = "📦 *Mahsulotlarimiz:*\n\n"
    for i, m in enumerate(mahsulotlar, 1):
        matn += f"{i}. {m['nomi']} — {m['narxi']}\n"
    await message.answer(matn, parse_mode="Markdown")

# === BUYURTMA ===
@dp.message(lambda m: m.text == "🛒 Buyurtma berish")
async def buyurtma(message: types.Message):
    await message.answer(
        "Buyurtma berish uchun quyidagi formatda yozing:\n\n"
        "📝 *Ism: ...*\n"
        "📱 *Telefon: ...*\n"
        "📦 *Mahsulot: ...*",
        parse_mode="Markdown"
    )

# === BOG'LANISH ===
@dp.message(lambda m: m.text == "📞 Bog'lanish")
async def boglanish(message: types.Message):
    await message.answer(
        f"📞 Admin bilan bog'lanish:\n{ADMIN_USERNAME}\n\n"
        "Ish vaqti: 9:00 — 18:00"
    )

# === BOSHQA XABARLAR (buyurtma qabul) ===
@dp.message()
async def buyurtma_qabul(message: types.Message):
    if any(x in message.text.lower() for x in ["ism:", "telefon:", "mahsulot:"]):
        await message.answer(
            "✅ Buyurtmangiz qabul qilindi!\n"
            "Tez orada admin siz bilan bog'lanadi."
        )
        # Adminga xabar yuborish
        await bot.send_message(
            chat_id=message.chat.id,  # bu yerga admin chat_id qo'ying
            text=f"🛒 Yangi buyurtma!\n\n{message.text}\n\nMijoz: @{message.from_user.username}"
        )
    else:
        await message.answer("Iltimos, menyudan foydalaning 👇", reply_markup=asosiy_menu())

# === ISHGA TUSHIRISH ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())