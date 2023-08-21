# from multiprocessing import Process
from threading import Thread
from scheduler import scheduler
import json
from configs import Configs_service
from bot import run_telegram_bot


    

server_details=open("./server_details.json")
server_details=json.load(server_details)
config_service=Configs_service(server_details=server_details)
TELEGRAM_TOKEN=server_details["TELEGRAM_TOKEN"]
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
CHAT_ID=server_details["CHAT_ID"]

if __name__ == "__main__":
    p1 = Thread(target=scheduler,args=(config_service,))
    p1.start()
    run_telegram_bot(config_service,TELEGRAM_API_URL,CHAT_ID,TELEGRAM_TOKEN)