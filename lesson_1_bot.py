# from aiogram import Bot, Dispatcher, types, executor
# from config import token


# bot = Bot(token=token)
# dp = Dispatcher(bot)

# @dp.message_handler(commands = 'start')
# async def start(message:types.Message):
#     await message.answer("привет мир!, тебя зовут нурай я угадал")


# @dp.message_handler(commands = 'help')
# async def help(message:types.Message):
#     await message.answer("Чем могу помочь?")

# @dp.message_handler(text = 'привет')
# async def hello(message:types.Message):
#     await message.answer("привет, как дела? ")


# @dp.message_handler(commands = 'test')
# async def test(message:types.Message):
#     await message.reply("Тестовое сообщение")
#     await message.answer_location(40.51933983835417, 72.80298453971301)
#     await message.answer_dice()
#     await message.answer_photo('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg4pQVpknqpc7o5Xy2QehuGrdmoGdAakwRXzpemsfK4oHSzua73Yj2q_GSGqIgxN0lsNs&usqp=CAU')
#     await message.answer_contact('+996755750238', 'Nurai', 'Temirbaeva')
#     with open('photo_2023-11-01_17-47-53.jpg', 'rb') as photo:
#         await message.answer_photo(photo)
    



# executor.start_polling(dp)







