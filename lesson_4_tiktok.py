# import requests , os

# input_url = input("URL video:")
# print(input_url)

# # https://www.tiktok.com/@geeks_osh/video/7293896300020403474
# # https://www.tiktok.com/@geeks_osh/video/7293896300020403474?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029
# # https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id=7285981472740101378

# split_url = input_url.split("/")
# print(split_url)
# current_id = split_url[5].split("?")[0]
# print(current_id)

# video_api = requests.get(f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}").json()
# # print(video_api)

# video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
# print(video_url)
# if video_url:
#     print("Скачиваем видео", video_api.get('aweme_list')[0].get('desc'))
#     title = video_api.get('aweme_list')[0].get('desc')
#     try:
#         os.mkdir('video')
#     except:
#         pass

#     try:
#         with open(f'video/{title}.mp4' ,'wb') as video_file:
#             video_file.write(requests.get(video_url).content)
#         print(f"Видео {title}.mp4 успешно скачан в папку video")
#     except Exception as error:
#         print(f"Error {error}")



# дз 
import requests 
from config import token
from aiogram import Bot,Dispatcher,types,executor
import random

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Здравструйте {message.from_user.full_name} ")
    await message.answer("Отправьте ссылку видео которую хотите скачать")
# https://www.tiktok.com/@geeks_osh/video/7293896300020403474
# https://www.tiktok.com/@geeks_osh/video/7293896300020403474?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029
# https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id=7285981472740101378



@dp.message_handler(commands='info')
async def info(message: types.Message):
    await message.answer("Подождите немного...")
    get_id_video = message.text.split('?')
    current_id = get_id_video[0].split('/')[5]
    
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    
    if 'aweme_list' in video_api:
        aweme = video_api['aweme_list'][0]
        desc_video = aweme.get('desc', 'Описание отсутствует')
        author = aweme.get('author', 'Автор неизвестен')
        
        await message.answer(f"Описание: {desc_video}")
        await message.answer(f"Автор: {author}")
    else:
        await message.answer("Не удалось получить информацию о видео.")

@dp.message_handler()
async def dowload_send_video(message:types.Message):
    await message.answer("Скачиваю видео...")
    get_id_video = message.text.split('?')
    current_id = get_id_video[0].split('/')[5]
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
    if video_url:
        title_video = video_api.get('aweme_list')[0].get('desc')
        print("скачиваем видео...")
        try:
            with open(f'video/{title_video}.mp4','wb') as video_file:
                video_file.write(requests.get(video_url).content)
            print('Видео успешно скачан в шапку video')
        except Exception as error:
            print(f'Error: {error}')
        try:
            with open(f'video/{title_video}.mp4', 'rb') as send_file:
                await message.answer_video(send_file)
        except Exception as error:
            await message.answer(f"Ошибка: {error}")
     

executor.start_polling(dp)


