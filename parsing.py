from bs4 import BeautifulSoup
import requests

url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
response = requests.get(url=url)
soup = BeautifulSoup(response.text, 'lxml')
all_current = soup.find_all('td', class_='exrate')
print(all_current)