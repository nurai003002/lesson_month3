import requests
import re

# Отправка GET-запроса
response = requests.get('https://vt.tiktok.com/ZSN5FLHme')
html_content = response.text

# Поиск идентификатора видео с помощью регулярного выражения
video_id_match = re.search(r'"id":"(\d+)"', html_content)

if video_id_match:
    video_id = video_id_match.group(1)
    print("ID видео:", video_id)
else:
    print("ID видео не найден")



