from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters
import json
from configs import Configs_service
from multiprocessing import Process
import schedule
from request import Request



server_details=open("./server_details.json")
server_details=json.load(server_details)
config_service=Configs_service(server_details=server_details)
TELEGRAM_TOKEN=server_details["TELEGRAM_TOKEN"]
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
CHAT_ID=server_details["CHAT_ID"]
request=Request()


schedule.every(15).minutes.do(config_service.update_configs)

def running_schedule():
    while True:
        schedule.run_pending()
        




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    image=open("./input_config.jpeg","rb")
    await update.message.reply_text(f' به قند بات خوش آمدید , با /config  و وارد کردن config خود پس از ان, از مدت زمان حجم و config جدید در صورت تغیرات در سرور مطلع شوید. در صورت هرگونه مشکل با ghand_sup@  در ارتباط باشد ')
    await update.message.reply_photo(photo=image,)    
    
async def get_details_by_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config_uri=update.message.text.replace("/config","").replace(" ","")
    formatter=config_service.find_config_by_uri(config_uri)
    details=formatter.send_config_details()
    for msg in details:
        await update.message.reply_text(msg)
    request.post_request(url=TELEGRAM_API_URL,body={"chat_id":CHAT_ID,"text":f'{formatter.config_name()} checked the config'})
        
async def get_details_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._chat_id == 6132337496:        
        config_remark=update.message.text.replace("/name","").replace(" ","")
        details=config_service.find_config_by_remark(config_remark).send_config_details()
        for msg in details:
            await update.message.reply_text(msg)
    else:
        await update.message.reply_text("shoma dastresi be in feature nadarid !!!")
        
async def update_configs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._chat_id == 6132337496:        
        config_service.update_configs()
        await update.message.reply_text("done!")
    else:
        await update.message.reply_text("shoma dastresi be in feature nadarid !!!")

async def config_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "vmess://" in update.message.text :
            formater=config_service.find_config_by_uri(update.message.text)
            details=formater.send_config_details()
            for msg in details:
                await update.message.reply_text(msg)
            request.post_request(url=TELEGRAM_API_URL,body={"chat_id":CHAT_ID,"text":f'{formater.config_name()} checked the config'})
    else :
        await update.message.reply_text("کانفیگ را به صورت زیر وارد کنید ")
        await update.message.reply_text("/config vmess://eyh....")
    
        
        
    
def run_telegram_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("config",get_details_by_config))
    app.add_handler(CommandHandler("name",get_details_by_name))
    app.add_handler(CommandHandler("update",update_configs))
    app.add_handler(MessageHandler(filters.TEXT,config_message_handler))
    app.run_polling()


if __name__ == "__main__":
    p1 = Process(target=running_schedule)
    p1.start()
    p2 = Process(target=run_telegram_bot)
    p2.start()
    p1.join()
    p2.join()
    

    
    


    
    
    

