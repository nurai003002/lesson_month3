from aiogram import Bot, Dispatcher, types, executor
from config import token
import random

bot = Bot(token=token)
dp = Dispatcher(bot)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                              


rand = random.randint(1,3)
@dp.message_handler(commands='start')
async def start(message: types.Message):
   await message.answer("Я загадал число от 1,3")
   await message.answer_photo("https://ruinterbiz.ru/wp-content/uploads/2018/05/mema-rjak.gif")
   

@dp.message_handler()
async def num(message: types.Message):
    print(message)
    if int(message.text) == rand:
      await message.answer("Все таки угадал!")
      await message.answer_photo("https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg")
    else:
      await message.reply("Уверен?")
      await message.answer_photo("https://media.makeameme.org/created/sorry-you-lose.jpg")
      

executor.start_polling(dp)

