from config import token
from aiogram import Bot,Dispatcher,types,executor
import requests 
import logging, os
from bs4 import BeautifulSoup


bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}/laptops")
@dp.message_handler(commands='laptops')
async def send_laptops(message:types.Message):
    await message.answer("ОТправляю наутбуки в наличии....")

    n = 0
    for page in range(1,7):
            url = f'https://www.sulpak.kg/f/noutbuki?page={page}'
            response = requests.get(url=url)
            print(response)
            soup = BeautifulSoup(response.text, 'lxml')
            all_laptops = soup.find_all('div', class_='product__item-name')
            all_prices = soup.find_all('div', class_='product__item-price')


            for laptop, price in zip(all_laptops, all_prices):
                n+=1
                print(n,laptop.text,"".join(price.text.split()))
                price_laptop = " ".join(price.text.split())
                await message.answer(f"{n} {laptop.text} {price_laptop}")
    await message.answer("вот все ноутбуки в наличии")
    
    
executor.start_polling(dp)



