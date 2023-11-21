from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config import token
import sqlite3, time,uuid, os, telebot

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)
      
connect = sqlite3.connect('customs.db', check_same_thread=False)
cursor = connect.cursor()


cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
               id INTEGER RRIMARY KEY,
               user_name VARCHAR (200),
               first_name VARCHAR (200),
               last_name VARCHAR (200),
               created VARCHAR (100)
);""")

cursor.execute(""" CREATE TABLE IF NOT EXISTS receipt(
               payment_code INT,
               first_name VARCHAR (200),
               last_name VARCHAR (200),
               direction  VARCHAR (200),
               amount INT,
               date VARCHAR (100)
                 
);""")




start_buttons =[
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Контакты"),
    types.KeyboardButton("Курсы"),
    types.KeyboardButton("Оплатить")
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    cursor.execute("SELECT * FROM users WHERE user_name = ?", (message.from_user.username,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        cursor.execute("INSERT INTO users (id,user_name, first_name, last_name, created) VALUES (?, ?, ?, ?, ?);",
                   (message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, time.ctime()))
    connect.commit()
    await message.answer("Привет, добро пожаловать в курсы Geeks", reply_markup=start_keyboard)


@dp.message_handler(text = 'О нас')
async def about_us(message: types.Message):
    await message.answer("Geeks - это курсы в Бишкеке, Кара-Балте и Ош созданное в 2019 году")


@dp.message_handler(text = 'Адрес')
async def address(message: types.Message):
    await message.reply("Наш адресс: \n Мырзалы Аматова 1Б (БЦ Томирис) ")
    await message.answer_location(40.51933983835417, 72.80298453971301)


@dp.message_handler(text = "Контакты")
async def conntect(message: types.Message):
    await message.answer("Наши контакты: ")
    await message.answer_contact("+996777123123", "Nurbolot", "Erkinbaev")
    await message.answer_contact("+996777123120", "Ulan", "Ashirov")

courses_buttons =[
    types.KeyboardButton("Backend"),
    types.KeyboardButton("Frontend"),
    types.KeyboardButton("UX-UI"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("iOS"),
    types.KeyboardButton("Назад")
    

]
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)

@dp.message_handler(text = "Курсы")
async def courses(message: types.Message):
    await message.answer("Вот наши курсы: ", reply_markup=courses_keyboard)


@dp.message_handler(text = "Backend")
async def backend(message: types.Message):
    await message.reply("Backend - это внутренный  вид сайта, невидименый глазу человека")
    await message.answer("https://thecode.media/backend/")


@dp.message_handler(text = "Frontend")
async def frontend(message: types.Message):
    await message.reply("Frontend - это внешний вид сайта.\n Разработчики этоого направления отвечают за внешний вид сайта\n подрбнее -> https://brunoyam.com/blog/programmirovanie/front-end")


@dp.message_handler(text = "UX-UI")
async def uxui(message: types.Message):
    await message.reply("UX-UI - это красота сайта, \n разработчики этого направиления создают дизайн сайта или приложения\nподрбнее -> https://netology.ru/blog/06-2022-ux-ui-designer")


@dp.message_handler(text = "Android")
async def android(message: types.Message):
    await message.reply("Android - это направление для создание приложений под анроид \n подрбнее -> https://www.profguide.io/professions/android_developer.html")


@dp.message_handler(text = "iOS")
async def ios(message: types.Message):
    await message.reply("iOS - это направление для создание приложений под ios то есть для пользователей Apple \n Также подробнее -> https://blog.skillfactory.ru/kto-takoj-ios-razrabotchik/")

@dp.message_handler(text = 'Оплатить')
async def pay(message: types.Message):
    await message.answer("Введите эту комманду, чтобы оплатить /receipt")
    
@dp.message_handler(text = "Назад")
async def cancell(message: types.Message):
    await start(message)

class ReceiptState(StatesGroup):
    first_name = State()
    last_name = State()
    direction = State()
    amount = State()

@dp.message_handler(commands="receipt")
async def get_receipt(message: types.Message):
    await message.answer("Для генерации чека введите следующие данные: \n (Имя, Фамилия, Направление, Сумма)")
    await message.answer("Введите свое имя: ")
    await ReceiptState.first_name.set()


@dp.message_handler(state=ReceiptState.first_name)
async def get_last_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name= message.text)
    await message.answer("Введите свою фамилию: ")
    await ReceiptState.last_name.set()

@dp.message_handler(state=ReceiptState.last_name)
async def get_direction(message: types.Message, state: FSMContext):
    await state.update_data(last_name = message.text)
    await message.answer("Введите выбранное направление: ")
    await ReceiptState.direction.set()


@dp.message_handler(state=ReceiptState.direction)
async def get_amount(message: types.Message, state: FSMContext):
    await state.update_data(direction = message.text)
    await message.answer("Введите сумму оплаты: ")
    await ReceiptState.amount.set()
    
@dp.message_handler(state=ReceiptState.amount)
async def generate_receipt(message:types.Message, state:FSMContext):
    await state.update_data(amount=message.text)
    result = await storage.get_data(user=message.from_user.id)
    generate_payment_code = int(str(uuid.uuid4().int)[:10])
    print(generate_payment_code)
    print(result)
    cursor.execute(f"""INSERT INTO receipt (payment_code, first_name, last_name, direction, amount, date)
                   VALUES (?, ?, ?, ?, ?, ?);""", 
                   (generate_payment_code, result['first_name'], result['last_name'],
                    result['direction'], result['amount'], time.ctime()))
    connect.commit()
    await message.answer(f"""Чек об оплате курса {result['direction']}
""")
    await message.answer("Генерирую PDF файл...\nPDF файл с чеком успешно сгенерирован")


    pdf_filename = f"receipt_{generate_payment_code}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"Direction: {result['direction']}")
    c.drawString(100, 730, f"First Name: {result['first_name']}")
    c.drawString(100, 710, f"Last Name: {result['last_name']}")
    c.drawString(100, 690, f"Payment Code: {generate_payment_code}")
    c.drawString(100, 670, f"Date: {time.ctime()}")
    c.save()


    with open(pdf_filename, 'rb') as pdf_file:
        await message.answer_document(pdf_file)

    await bot.send_message(-4037053389,f"""Чек об оплате курса {result['direction']}
Имя: {result['first_name']}
Фамилия: {result['last_name']}
Код оплаты: {generate_payment_code}
Дата: {time.ctime()}""")
    
    with open(pdf_filename, 'rb') as pdf_file:
        await bot.send_document( -4037053389 ,pdf_file)
    


    os.remove(pdf_filename)

@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял, введите /start")


executor.start_polling(dp)

