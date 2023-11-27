import requests, schedule, time

def perform_request():
    try:
        url = input("Введите URL: ")
        response = requests.get(url=url)
        with open('url_logs.txt', 'a+', encoding='UTF - 8') as write_file:
            write_file.write(response.text + '\n\n\n')
    except:
        print("Ошибка!")


def main():
    perform_request()    
    schedule.every(1).minutes.do(perform_request)

    while True:
        schedule.run_pending()
        time.sleep(1)
main()

