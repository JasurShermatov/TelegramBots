import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session import aiohttp
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp.pytest_plugin import AiohttpClient
from pip._internal import locations

TOKEN = "7251423283:AAFm4BByf7orMbJPQyvpFfHU_LI8k4JP7iU"

dp = Dispatcher()

# Ma'lumotlarni saqlash uchun dictionary
data = {
    "🏢Kompaniyamiz haqida?": "Kompaniyamiz 2020-yilda tashkil topgan bo’lib, "
    "tezda mijozlar orasida mashhurlikka erishdi. Biz yuqori sifatli fast food mahsulotlari va "
    "xizmatlarini taklif etamiz. Mijozlarimizning ehtiyojlarini qondirishga intilib, innovatsion yondashuvimiz bilan ajralib turamiz.!",
    "📍Filiallarimiz?": "Bizning filiallarimiz Toshkent shaxar:  "
                       "Filial 1: Amir Temur ko'chasi,10"
                       "Filial 2: Chilonzor ko'chasi, 45"
                       "Filial 3: Yunusobod ko'chasi, 12"
                       "Filial 4: Sergeli ko'chasi, 8",
    "🖥️Buyurtma berish": {
        "🍔 Burger :25.000": "Siz Burger buyurtma qildingiz!",
        "🍕 Pizza": "Siz Pizza buyurtma qildingiz!",
        "🌯 Lavash": "Siz Lavash buyurtma qildingiz!",
        "🥪 Club sendvich": "Siz Club sendvich buyurtma qildingiz!",
        "🌭 Hot Dog": "Siz Hot Dog buyurtma qildingiz!",
        "🍟 Fries": "Siz Fries buyurtma qildingiz!"
    },
    "🗞️Yangiliklar": "Biz 4 yil ichida Toshkent shahrida 5 ta filial ochishga erishdik. "
     "Bu bizning maqsadlarimizning bir qismi edi. Keyingi 2 yil ichida filiallarimiz sonini 2X ga oshirmoqchimiz!",
    "📞Kontaktlar/Manzil": "☺️Biz ga qo'ng'iroq qiling\n "
                          "\n 📞+998 (977722146)\n 📞+998 (774442146) "
                          "\n"
                          "\n ⏰Ish soatlari:\n"
                          "Dush-Juma: 10:00 - 20:00\nShan-Yaksh:Yopiq!",
    "🇺🇿/🇷🇺Til": " Hozircha faqat uzbek tili mavjud!"
}



# Filiallarning joylashuvi
locations = {
    "Filial 1": {
        "name": "Navoi ko'chasi, 25",
        "latitude": 41.315591,  # Navoi ko'chasi koordinatalari
        "longitude": 69.292328
    },
    "Filial 2": {
        "name": "Chilonzor ko'chasi, 45",
        "latitude": 41.288567,
        "longitude": 69.228596
    },
    "Filial 3": {
        "name": "Yunusobod ko'chasi, 12",
        "latitude": 41.356500,
        "longitude": 69.204317
    },
    "Filial 4": {
        "name": "Sergeli ko'chasi, 8",
        "latitude": 41.244513,
        "longitude": 69.163866
    },
    "Filial 5": {
        "name": "Mirzo Ulug'bek ko'chasi, 22",
        "latitude": 41.338249,
        "longitude": 69.284843
    },
    "Filial 6": {
        "name": "Mustaqillik ko'chasi, 14",
        "latitude": 41.312445,
        "longitude": 69.243760
    },
    "Filial 7": {
        "name": "Beruniy ko'chasi, 7",
        "latitude": 41.334750,
        "longitude": 69.180330
    },
    "Filial 8": {
        "name": "Beshyog'och ko'chasi, 5",
        "latitude": 41.316021,
        "longitude": 69.266600
    }
}





@dp.message(CommandStart())
async def option_handler(message: types.Message) -> None:
    design = [
        [KeyboardButton(text="🏢Kompaniyamiz haqida?"), KeyboardButton(text="📍Filiallarimiz?")],
        [KeyboardButton(text="🖥️Buyurtma berish")],
        [KeyboardButton(text="🗞️Yangiliklar")],
        [KeyboardButton(text="📞Kontaktlar/Manzil"), KeyboardButton(text="🇺🇿/🇷🇺Til")]
    ]
    rkm = ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
    await message.answer("Tanlov qiling!", reply_markup=rkm)




# "📍Filiallarimiz?" tugmasi bosilganda inline keyboard yaratamiz
@dp.message(F.text == "📍Filiallarimiz?")
async def location_handler(message: types.Message) -> None:

    # Tugmalar dizayni
    filial_buttons = [
        [KeyboardButton(text="🚩Navoi ko'chasi, 25"), KeyboardButton(text="🚩Chilonzor ko'chasi, 45")],
        [KeyboardButton(text="🚩Yunusobod ko'chasi, 12"), KeyboardButton(text="🚩Sergeli ko'chasi, 8")],
        [KeyboardButton(text="🚩Mirzo Ulug'bek ko'chasi, 22"), KeyboardButton(text="🚩Mustaqillik ko'chasi, 14")],
        [KeyboardButton(text="🚩Beruniy ko'chasi, 7"), KeyboardButton(text="🚩Beshyog'och ko'chasi, 5")],
        [KeyboardButton(text="• 🔙 Ortga qaytish")]
    ]

    rkb = ReplyKeyboardMarkup(keyboard=filial_buttons,  resize_keyboard=True)
    await message.answer("Tanlov qiling!", reply_markup=rkb)

# Dinamik ravishda location tugmalarini qayta ishlaydigan handler
@dp.message(F.text.startswith("🚩"))
async def send_location(message: types.Message) -> None:

    location_name = message.text.replace("🚩", "").strip()
    # locations lug'atidan tegishli manzilni topamiz
    for filial, info in locations.items():
        # Qo'shimcha bo'sh joylarni olib tashlab, nomlarni solishtirish
        if info["name"].strip() == location_name:
            # Manzil nomi va joylashuvini yuborish
            await message.answer(f"Manzil: {info['name']}")
            await message.answer_location(latitude=info['latitude'], longitude=info['longitude'])
            break
    else:
        # Agar nom topilmasa, xato xabarini yuborish
        await message.answer("Manzil topilmadi!")



# Kontaktlar/Manzil tugmasi bosilganda telefon raqamini va joylashuvni yuborish
@dp.message(F.text == "📞Kontaktlar/Manzil")
async def contact_info_handler(message: types.Message) -> None:
    # Telefon raqamini yuboring
    await message.answer(data["📞Kontaktlar/Manzil"])
    # Joylashuvni avtomatik yuborish (masalan, Toshkent shahridagi manzil)
    await message.answer_location(latitude=41.2995, longitude=69.2401)  # Toshkent shahrining koordinatalari




# Yangiliklar tugmasi bosilganda javob berish
@dp.message(F.text == "🗞️Yangiliklar")
async def news_handler(message: types.Message) -> None:
    await message.answer(data["🗞️Yangiliklar"])




# kompaniya button uchun filter
@dp.message(F.text == "🏢Kompaniyamiz haqida?")
async def company_info_handler(message: types.Message) -> None:
    try:
        photo_url = "https://raw.githubusercontent.com/JasurShermatov/logo/refs/heads/main/photo_2024-09-28_11-39-14.jpg"  #kompaniya rasmining url linki
        text = data["🏢Kompaniyamiz haqida?"]    # tepada kompaniya haqida text malumot
        telegram_link = "Batafsil👇\n[Telegram akkauntim.](https://t.me/Shermatov_J05)"  # Bu yerda Telegram akkauntimga havola

        await message.answer_photo(photo=photo_url, caption=text + "\n\n" + telegram_link, parse_mode='Markdown')  # Rasm va matnni bir joyda yuborish
    except Exception as e:
        await message.answer("Rasm yuborishda xatolik yuz berdi: " + str(e))






# Narxlarni saqlash uchun global o'zgaruvchilar
total_price = 0  # Umumiy narxni saqlash uchun o'zgaruvchi
ordered_items = {}  # Buyurtma qilingan mahsulotlar ro'yxati (miqdor bilan)

# Buyurtma berish tugmasini bosgand-a ovqat tanlash bo'limini chiqaradi
@dp.message(F.text == "🖥️Buyurtma berish")
async def order_handler(message: types.Message) -> None:
    food_buttons = [
        [KeyboardButton(text="🍔 Burger: 35.000"), KeyboardButton(text="🍕 Pizza: 40.000")],
        [KeyboardButton(text="🌯 Lavash : 30.000"), KeyboardButton(text="🥪 Club sendvich : 30.000")],
        [KeyboardButton(text="🌭 Hot Dog : 20.000"), KeyboardButton(text="🍟 Fries : 15.000")],
        [KeyboardButton(text="✅ Buyurtmani yakunlash")],
        [KeyboardButton(text="• 🔙 Ortga qaytish")]
    ]
    rkm = ReplyKeyboardMarkup(keyboard=food_buttons, resize_keyboard=True)
    await message.answer("Buyurtma berishingiz mumkin!!!", reply_markup=rkm)

# Ovqatni tanlagandan keyin javob berish
@dp.message(F.text.in_(["🍔 Burger: 35.000", "🍕 Pizza: 40.000", "🌯 Lavash : 30.000",
                        "🥪 Club sendvich : 30.000", "🌭 Hot Dog : 20.000",
                        "🍟 Fries : 15.000"]))
async def food_selection_handler(message: types.Message) -> None:
    global total_price
    global ordered_items

    selected_food = message.text
    food_name = selected_food.split(":")[0].strip()  # Ovqat nomi
    food_price = int(selected_food.split(": ")[1].replace(".", "").replace(",", "").strip())  # Narx

    # Buyurtmaga ovqat qo'shamiz
    if food_name in ordered_items:
        ordered_items[food_name] += 1  # Miqdorni oshirish
    else:
        ordered_items[food_name] = 1  # Yangi ovqat qo'shish

    total_price += food_price  # Umumiy narxni yangilaymiz

    response = f"{food_name} buyurtma qilindi. Narxi: {food_price} so'm. Jami: {ordered_items[food_name]} ta."
    await message.answer(response)

# Buyurtmani yakunlash
@dp.message(F.text == "✅ Buyurtmani yakunlash")
async def finalize_order(message: types.Message) -> None:
    global total_price
    global ordered_items

    if not ordered_items:
        await message.answer("Siz hech qanday buyurtma qilmagansiz!")
        return

    # Buyurtma haqida xabar
    order_summary = "\n".join([f"{item}: {quantity} ta" for item, quantity in ordered_items.items()])
    await message.answer(f"Sizning buyurtmangiz:\n{order_summary}\n\nUmumiy narx: {total_price} so'm\nHaridingiz uchun raxmat☺️")

    # Narxni reset qilamiz va buyurtmalar ro'yxatini tozalaymiz
    total_price = 0
    ordered_items = {}

    await back_to_menu_handler(message)


# "Ortga qaytish" tugmasi bosilganda asosiy menyuga qaytish
@dp.message(F.text == "• 🔙 Ortga qaytish")
async def back_to_menu_handler(message: types.Message) -> None:
    design = [
        [KeyboardButton(text="🏢Kompaniyamiz haqida?"), KeyboardButton(text="📍Filiallarimiz?")],
        [KeyboardButton(text="🖥️Buyurtma berish")],
        [KeyboardButton(text="🗞️Yangiliklar")],
        [KeyboardButton(text="📞Kontaktlar/Manzil"), KeyboardButton(text="🇺🇿/🇷🇺Til")]
    ]
    rkm = ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
    await message.answer("Asosiy menyuga qaytdingiz", reply_markup=rkm)




# Tugmalar ustiga bosilganda javob berish
@dp.message(F.text.in_(data.keys()))
async def button_handler(message: types.Message):
    response = data.get(message.text, "Noma'lum tanlov, /start buyrug'ini yozing!")
    await message.answer(response)




# /help komandasi!!!
@dp.message(Command("help"))
async def menu_handler(message: Message) -> None:
    await message.answer("/start buyrug'ini yozing!")




@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")




async def main() -> None:
    P = "http://proxy.server:3128"
    session = AiohttpSession(proxy=P)
    bot = Bot(token=TOKEN, session = session,  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

