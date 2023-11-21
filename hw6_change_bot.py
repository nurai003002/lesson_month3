import os, logging,requests
from aiogram import Bot, Dispatcher, types, executor
from bs4 import BeautifulSoup
from config import token
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

inline_buttons = [
    InlineKeyboardButton("USD", callback_data='usd'),
    InlineKeyboardButton("RUB", callback_data= 'rub'),
    InlineKeyboardButton("EURO", callback_data= 'eur'),
    InlineKeyboardButton("KZT", callback_data= 'kzt')
]
keyboard_inline = InlineKeyboardMarkup().add(*inline_buttons)

class Current(StatesGroup):
    money = State()



@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}")
    await message.answer(f"Вы можете посмотреть и перевести волюты\n Введите сумму:")
    await Current.money.set()

@dp.message_handler(state = Current.money)
async def money(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await message.answer("Значение сохранено. Выберите валюту для обмена.", reply_markup=keyboard_inline)
    await Current.next()



@dp.callback_query_handler(lambda call: call.data == "usd")
async def usd_current(call: types.CallbackQuery, state: FSMContext):
    await usd(call.message, state)

@dp.message_handler(commands='usd', state=Current.money)
async def usd(message: types.Message, state: FSMContext):
    url = "https://www.nbkr.kg/index.jsp?lang=RUS"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "lxml")
    all_current = soup.find_all('td', class_='exrate')
    usd = float(all_current[0].text.replace(',', '.'))
    data = await state.get_data()
    money = data.get('money')

    if money is not None:
        try:
            money = float(money)
            result = money * usd
            await message.answer(f"Результат - KRG-USD: {result}")
        except ValueError:
            await message.answer("Введено некорректное значение денег")
    else:
        await message.answer("Не удалось получить значение денег")

    await state.finish()
###################################3

@dp.callback_query_handler(lambda call: call.data == "eur")
async def eur_current(call: types.CallbackQuery, state: FSMContext):
    await eur(call.message, state)

@dp.message_handler(commands="eur", state=Current.money)
async def eur(message: types.Message, state: FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_current = soup.find_all('td', class_='exrate')
    eur = float(all_current[2].text.replace(',', '.'))

    data = await state.get_data()
    money = data.get('money')

    if money is not None:
        try:
            money = float(money)
            result = money * eur
            await message.answer(f"Результат - KRG-EURO: {result}")
        except ValueError:
            await message.answer("Введено некорректное значение денег")
    else:
        await message.answer("Не удалось получить значение денег")

    await state.finish()

# ##########################3


@dp.callback_query_handler(lambda call: call.data == "rub")
async def rub_current(call: types.CallbackQuery, state: FSMContext):
    await rub(call.message, state)

@dp.message_handler(commands="rub", state=Current.money)
async def rub(message: types.Message, state: FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_current = soup.find_all('td', class_='exrate')
    rub = float(all_current[4].text.replace(',', '.'))

    data = await state.get_data()
    money = data.get('money')

    if money is not None:
        try:
            money = float(money)
            result = money * rub
            await message.answer(f"Результат - RUB-KRG: {result}")
        except ValueError:
            await message.answer("Введено некорректное значение денег")
    else:
        await message.answer("Не удалось получить значение денег")

    await state.finish()

########################333

@dp.callback_query_handler(lambda call: call.data == "kzt")
async def kzt_current(call: types.CallbackQuery, state: FSMContext):
    await kzt(call.message, state)

@dp.message_handler(commands="kzt", state=Current.money)
async def kzt(message: types.Message, state: FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_current = soup.find_all('td', class_='exrate')
    kzt = float(all_current[6].text.replace(',', '.'))

    data = await state.get_data()
    money = data.get('money')

    if money is not None:
        try:
            money = float(money)
            result = money * kzt
            await message.answer(f"Резальтат - KRG-KZT: {result}")
        except ValueError:
            await message.answer("Введено некорректное значение денег")
    else:
        await message.answer("Не удалось получить значение денег")

    await state.finish()



executor.start_polling(dp)
