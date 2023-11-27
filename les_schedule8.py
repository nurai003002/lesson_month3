import schedule
import time, requests

# def job():
#     print("Working....", time.ctime())


# def notification_lesson_12_2b():
#     print("Здравствйте, сегодня у вас урок в 16:00")


# # schedule.every(2).seconds.do(job)
# # schedule.every(1).minutes.do(job)
# # schedule.every().saturday.at("16:24").do(job)
# # schedule.every().saturday.at("16:27").do(notification_lesson_12_2b)
# # schedule.every().saturday.at("16:29", 'Asia/Bishkek').do(notification_lesson_12_2b)
# schedule.every(2).seconds.do(job)
# schedule.every(3).seconds.do(notification_lesson_12_2b)


# main code
def current_btc_price():
    url  = " https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    respose = requests.get(url=url).json()  
    # print(respose)
    json_key = list(respose.values())
    index = json_key[1]
    # print(index)

    with open("btc_logs.txt", "a+" ) as write_file:
        write_file.write(f"{index} {time.ctime()}\n")   
   
schedule.every(3).seconds.do(current_btc_price)

# ""Курманбек агай`s code"""

# # def write_txt_btc():
#     url = "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
#     response = requests.get(url=url).json()
#     with open("btc_logs.txt", "a+") as logs:
#         logs.write(f"{response.get('price')} {time.ctime()}\n")
  
# schedule.every(3).seconds.do(write_txt_btc)



while True:
    schedule.run_pending()
    time.sleep(1)



    
