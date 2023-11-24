from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token
import logging

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

start_buttons =[
    types.KeyboardButton("Отправить номер: ", request_contact=True),
    types.KeyboardButton("Отправить локацию: ", request_location=True),
    types.KeyboardButton("Отправить сообщение ")
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup= start_keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_content(message: types.Message):
    await message.answer(f"{message.contact.phone_number}")

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(message: types.Message):
    await message.answer(f"{message.location}")


anonim_select_buttons = [
    types.InlineKeyboardButton("Да", callback_data='select_yes'),
    types.InlineKeyboardButton("Нет", callback_data='select_no')
]

anonim_select_keyboard = types.InlineKeyboardMarkup().add(*anonim_select_buttons)


@dp.message_handler(text= 'Отправить сообщение')
async def send_anonim(message: types.Message):
    await message.answer(f"Вы хотите отправить анонимное сообщение?", reply_markup=anonim_select_keyboard)

@dp.callback_query_handler(lambda call: call.data == 'select_no')
async def select_no_answer(message: types.CallbackQuery):
    await message.answer("Окей")
    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)

class AnonimState(StatesGroup):
    message = State()


@dp.callback_query_handler(lambda call: call.data == 'select_yes')
async def select_yes_answer(message: types.CallbackQuery):
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                             text = "Напишите свое сообщение и мы отправим его в группу")
    await AnonimState.message.set()

@dp.message_handler(state = AnonimState)
async def send_message_group(message: types.Message, state: FSMContext):
    await message.answer("Отправляем сообщение....")
    await bot.send_message(chat_id= -4037053389, text=message.text)
    await message.answer("Отправил сообщение")
    await state.finish()

executor.start_polling(dp, skip_updates=True)
