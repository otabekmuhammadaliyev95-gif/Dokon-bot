import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

# ==============================
# SOZLAMALAR
# ==============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@Muhammadaliyev9"
ADMIN_IDS = [7185012024]  # ← O'z Telegram ID'ingizni kiriting!

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ==============================
# MA'LUMOTLAR
# ==============================
mahsulotlar = [
    {"nomi": "Mahsulot 1", "narxi": "50,000 so'm"},
    {"nomi": "Mahsulot 2", "narxi": "80,000 so'm"},
    {"nomi": "Mahsulot 3", "narxi": "120,000 so'm"},
]

users_db: dict = {}        # {user_id: {"name": ..., "username": ...}}
banned_users: set = set()  # ban qilingan user_id lar
orders: list = []          # buyurtmalar

# ==============================
# FSM STATES
# ==============================
class AdminStates(StatesGroup):
    broadcast = State()
    ban_user  = State()

# ==============================
# KLAVIATURALAR
# ==============================
def asosiy_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📦 Mahsulotlar"))
    kb.add(KeyboardButton("🛒 Buyurtma berish"))
    kb.add(KeyboardButton("📞 Bog'lanish"))
    return kb

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("👥 Foydalanuvchilar"), KeyboardButton("📊 Statistika"))
    kb.add(KeyboardButton("📢 Broadcast"),        KeyboardButton("🚫 Ban qilish"))
    kb.add(KeyboardButton("✅ Banned ro'yxat"),   KeyboardButton("📋 Buyurtmalar"))
    kb.add(KeyboardButton("🔙 Asosiy menyu"))
    return kb

# ==============================
# YORDAMCHI
# ==============================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def register_user(user: types.User):
    if user.id not in users_db:
        users_db[user.id] = {
            "name": user.full_name,
            "username": user.username or "Yoq",
        }

# ==============================
# /start
# ==============================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    register_user(message.from_user)

    if message.from_user.id in banned_users:
        return await message.answer("Siz botdan ban qilingansiz.")

    await message.answer(
        "Assalomu alaykum! Do'konimizga xush kelibsiz\nQuyidagi menyudan tanlang:",
        reply_markup=asosiy_menu()
    )

# ==============================
# /admin
# ==============================
@dp.message_handler(commands=["admin"])
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("Sizda admin huquqi yoq.")

    await message.answer(
        "<b>Admin Panel</b>\nXush kelibsiz!",
        parse_mode="HTML",
        reply_markup=admin_menu()
    )

# ==============================
# ASOSIY MENYU
# ==============================
@dp.message_handler(lambda m: m.text == "📦 Mahsulotlar")
async def mahsulotlar_royxati(message: types.Message):
    register_user(message.from_user)
    matn = "📦 *Mahsulotlarimiz:*\n\n"
    for i, m in enumerate(mahsulotlar, 1):
        matn += f"{i}. {m['nomi']} — {m['narxi']}\n"
    await message.answer(matn, parse_mode="Markdown")

@dp.message_handler(lambda m: m.text == "🛒 Buyurtma berish")
async def buyurtma(message: types.Message):
    register_user(message.from_user)
    await message.answer(
        "Buyurtma berish uchun quyidagi formatda yozing:\n\n"
        "📝 *Ism: ...*\n"
        "📱 *Telefon: ...*\n"
        "📦 *Mahsulot: ...*",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda m: m.text == "📞 Bog'lanish")
async def boglanish(message: types.Message):
    register_user(message.from_user)
    await message.answer(
        f"📞 Admin bilan bog'lanish:\n{ADMIN_USERNAME}\n\nIsh vaqti: 9:00 — 18:00"
    )

# ==============================
# ADMIN PANEL
# ==============================

@dp.message_handler(lambda m: m.text == "👥 Foydalanuvchilar")
async def admin_users(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    if not users_db:
        return await message.answer("Hali foydalanuvchi yoq.")

    matn = "👥 <b>Foydalanuvchilar:</b>\n\n"
    for uid, u in list(users_db.items())[:30]:
        status = "🚫" if uid in banned_users else "✅"
        matn += f"{status} <b>{u['name']}</b> | @{u['username']} | <code>{uid}</code>\n"
    await message.answer(matn, parse_mode="HTML")

@dp.message_handler(lambda m: m.text == "📊 Statistika")
async def admin_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    total    = len(users_db)
    banned   = len(banned_users)
    active   = total - banned
    n_orders = len(orders)

    await message.answer(
        "📊 <b>Bot Statistikasi</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{total}</b>\n"
        f"✅ Faol: <b>{active}</b>\n"
        f"🚫 Ban: <b>{banned}</b>\n"
        f"🛒 Buyurtmalar: <b>{n_orders}</b>",
        parse_mode="HTML"
    )

@dp.message_handler(lambda m: m.text == "📢 Broadcast")
async def admin_broadcast_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await AdminStates.broadcast.set()
    await message.answer(
        "📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing:\n"
        "<i>Bekor qilish: /cancel</i>",
        parse_mode="HTML"
    )

@dp.message_handler(state=AdminStates.broadcast)
async def admin_broadcast_send(message: types.Message, state: FSMContext):
    await state.finish()
    sent = failed = 0
    for uid in users_db:
        if uid in banned_users:
            continue
        try:
            await bot.copy_message(uid, message.chat.id, message.message_id)
            sent += 1
        except Exception:
            failed += 1
    await message.answer(
        f"📢 <b>Broadcast tugadi!</b>\n\n✅ Yuborildi: <b>{sent}</b>\n❌ Xato: <b>{failed}</b>",
        parse_mode="HTML",
        reply_markup=admin_menu()
    )

@dp.message_handler(lambda m: m.text == "🚫 Ban qilish")
async def admin_ban_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await AdminStates.ban_user.set()
    await message.answer(
        "🚫 Ban/Unban qilish uchun foydalanuvchi <b>Telegram ID</b>sini yuboring:\n"
        "<i>Bekor qilish: /cancel</i>",
        parse_mode="HTML"
    )

@dp.message_handler(state=AdminStates.ban_user)
async def admin_ban_process(message: types.Message, state: FSMContext):
    try:
        target_id = int(message.text.strip())
    except ValueError:
        return await message.answer("Notogri ID! Faqat raqam kiriting.")
    if target_id in ADMIN_IDS:
        await state.finish()
        return await message.answer("Adminni ban qilib bolmaydi!", reply_markup=admin_menu())
    await state.finish()
    if target_id in banned_users:
        banned_users.discard(target_id)
        await message.answer(
            f"✅ <code>{target_id}</code> — <b>unban</b> qilindi.",
            parse_mode="HTML", reply_markup=admin_menu()
        )
    else:
        banned_users.add(target_id)
        await message.answer(
            f"🚫 <code>{target_id}</code> — <b>ban</b> qilindi.",
            parse_mode="HTML", reply_markup=admin_menu()
        )

@dp.message_handler(lambda m: m.text == "✅ Banned ro'yxat")
async def admin_banned_list(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    if not banned_users:
        return await message.answer("Ban qilingan foydalanuvchilar yoq.")
    matn = "🚫 <b>Ban qilinganlar:</b>\n\n"
    for uid in banned_users:
        u = users_db.get(uid)
        if u:
            matn += f"• <b>{u['name']}</b> | <code>{uid}</code>\n"
        else:
            matn += f"• <code>{uid}</code>\n"
    await message.answer(matn, parse_mode="HTML")

@dp.message_handler(lambda m: m.text == "📋 Buyurtmalar")
async def admin_orders(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    if not orders:
        return await message.answer("Hali buyurtma yoq.")
    matn = "📋 <b>So'nggi buyurtmalar:</b>\n\n"
    for i, o in enumerate(orders[-20:], 1):
        matn += (
            f"{i}. 👤 {o['name']} | 📱 {o['phone']}\n"
            f"   📦 {o['mahsulot']} | 🆔 <code>{o['user_id']}</code>\n\n"
        )
    await message.answer(matn, parse_mode="HTML")

@dp.message_handler(lambda m: m.text == "🔙 Asosiy menyu")
async def back_to_main(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=asosiy_menu())

@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    if is_admin(message.from_user.id):
        await message.answer("Bekor qilindi.", reply_markup=admin_menu())
    else:
        await message.answer("Bekor qilindi.", reply_markup=asosiy_menu())

# ==============================
# BUYURTMA QABUL QILISH
# ==============================
@dp.message_handler()
async def buyurtma_qabul(message: types.Message):
    register_user(message.from_user)

    if message.from_user.id in banned_users:
        return await message.answer("Siz botdan ban qilingansiz.")

    text = message.text.lower()
    if all(x in text for x in ["ism:", "telefon:", "mahsulot:"]):
        lines = message.text.split("\n")
        order = {"user_id": message.from_user.id, "name": "?", "phone": "?", "mahsulot": "?"}
        for line in lines:
            l = line.lower()
            if "ism:" in l:
                order["name"] = line.split(":", 1)[-1].strip()
            elif "telefon:" in l:
                order["phone"] = line.split(":", 1)[-1].strip()
            elif "mahsulot:" in l:
                order["mahsulot"] = line.split(":", 1)[-1].strip()
        orders.append(order)

        await message.answer("✅ Buyurtmangiz qabul qilindi!\nTez orada admin siz bilan bog'lanadi.")

        # Adminga bildirishnoma
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f"🛒 <b>Yangi buyurtma!</b>\n\n"
                    f"👤 Ism: {order['name']}\n"
                    f"📱 Telefon: {order['phone']}\n"
                    f"📦 Mahsulot: {order['mahsulot']}\n"
                    f"🆔 User ID: <code>{message.from_user.id}</code>",
                    parse_mode="HTML"
                )
            except Exception:
                pass
    else:
        await message.answer("Iltimos, menyudan foydalaning 👇", reply_markup=asosiy_menu())

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
