from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from configs import Configs_service
from multiprocessing import Process
import schedule




server_details=open("./server_details.json")
server_details=json.load(server_details)
config_service=Configs_service(server_details=server_details)
image=open("./input_config.jpeg","rb")


schedule.every(15).minutes.do(config_service.update_configs)

def running_schedule():
    while True:
        schedule.run_pending()
        



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    await update.message.reply_text(f' به قند بات خوش آمدید , با config/ و وارد کردن config خود پس از ان, از مدت زمان حجم و config جدید در صورت تغیرات در سرور مطلع شوید. در صورت هرگونه مشکل با ghand_sup@  در ارتباط باشد ')
    await update.message.reply_photo(photo=image,)    
    
async def get_details_by_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config_uri=update.message.text.replace("/config","").replace(" ","")
    details=config_service.find_config_by_uri(config_uri).send_config_details()
    for msg in details:
        await update.message.reply_text(msg)
        
async def get_details_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config_remark=update.message.text.replace("/name","").replace(" ","")
    details=config_service.find_config_by_remark(config_remark).send_config_details()
    for msg in details:
        await update.message.reply_text(msg)
    
def run_telegram_bot():
    app = ApplicationBuilder().token("6372238157:AAFesiFi15vJC7EaBveXqImnpBCbVyWxB50").build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("config",get_details_by_config))
    app.add_handler(CommandHandler("name",get_details_by_name))
    app.run_polling()


if __name__ == "__main__":
    p1 = Process(target=running_schedule)
    p1.start()
    p2 = Process(target=run_telegram_bot)
    p2.start()
    p1.join()
    p2.join()
    

    
    


    
    
    

