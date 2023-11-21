# парсинг - Для группировки данных
from bs4 import BeautifulSoup
import requests

# def parsing_askipress():
#     url = "https://akipress.org/"
#     response = requests.get(url=url)
#     print(response)
#     soup = BeautifulSoup(response.text, 'lxml')
#     # print(soup)
#     all_news = soup.find_all('a', class_= "newslink")
#     n = 0
#     print(all_news)
#     for news in all_news:
#         n +=1
#         print(f"{n}) {news.text}")
#         with open('news.txt', 'a+', encoding='UTF-8') as news_txt:
#             news_txt.write(f"{n}) {news.text}\n")


# parsing_askipress()

# def parsing_sulpak():
#     n = 0
#     for page in range(1,7):
#         url = f'https://www.sulpak.kg/f/noutbuki?page={page}'
#         response = requests.get(url=url)
#         print(response)
#         soup = BeautifulSoup(response.text, 'lxml')
#         all_laptops = soup.find_all('div', class_='product__item-name')
#         all_prices = soup.find_all('div', class_='product__item-price')
#         for laptop, price in zip(all_laptops, all_prices):
#             n+=1
#             print(n,laptop.text,"".join(price.text.split()))
            
#             # print(f" {a}) {laptop.text}")

# parsing_sulpak()

def current():
    url  = "https://www.nbkr.kg/index.jsp?lang=RUS"
    response = requests.get(url=url)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
    # currents = soup.find_all('')
current()
   