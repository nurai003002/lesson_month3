import sqlite3,logging
from aiogram import Bot, Dispatcher, types,executor
from aiogram.types import ParseMode
from config import token
logging.basicConfig(level=logging.INFO)


bot = Bot(token=token)
dp = Dispatcher(bot)

connect = sqlite3.connect("cars_check.db")
cursor = connect.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS cars(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               car_number TEXT,
               model TEXT,
               color TEXT,
               year INTEGER NOT NULL DEFAULT 0,
               price VARCHAR (150)
              
);""")

cars_list = [
    ("01KG710ANK", "Toyota Highlander III ","black", 2016, "27000$"),
    ("01KG718AAZ", "Lexus ES ","white", 2013, "21350 $"),
    ('01001ERA', 'BMW',  'blue', 2017, "27000$"),
    ('01100CTO', 'MERSEDES-BENS', 'BLACK', 1993,"27000$" ),
    ('02002OSH', 'FIT', 'blue', 2005, "27000$"),
    ('01063CLS', 'MERSEDES',  'WHILE', 2020, "27000$"),
    ('01100BRO', 'BMW',  'WHILE', 2022,  "27000$"),
    ('01777SEM', 'MERSEDES-BENS', 'WILE', 2015, "27000$" ),
    ('01001BEK', 'BMW', 'BLACK', 2022, "27000$" ),
    ('02002TWO', 'MERSEDES',  'YELLO', 2022,  "27000$")
]

cursor.executemany("""INSERT INTO cars (car_number, model, color, year, price) VALUES (?, ?, ?, ?, ?)""", cars_list)
connect.commit()

@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name} \nЗдесь вы можете найти машину введя его номер. \n Введите номер: ")


@dp.message_handler(lambda message: message.text.isalnum())
async def cars_check(message: types.Message):
    car_number = message.text.upper()
    cursor.execute("SELECT * FROM cars WHERE car_number = ?", (car_number,))
    car = cursor.fetchone()
   
#fetchall() – возвращает число записей в виде упорядоченного списка; fetchmany(size) – возвращает число записей не более size; fetchone() – возвращает первую запись.

    if car:
        response_info = f"Информация о   машине,\n которую вы искали:\n\nНомер: {car[1]}\nМодель: {car[2]}\nЦвет: {car[3]}\nГод: {car[4]}\nЦена: {car[5]}"
    else: 
        response_info = "Нет данных"

    await message.answer(response_info, parse_mode=ParseMode.MARKDOWN)


executor.start_polling(dp, skip_updates=True)

