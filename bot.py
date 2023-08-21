from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters
from request import Request

request=Request()



class Telegram_Bot():
    def __init__(self,config_service,telegram_api_url,chat_id):
        self.config_service=config_service
        self.telegram_api_url=telegram_api_url
        self.chat_id=chat_id
         
    
    async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        image=open("./input_config.jpeg","rb")
        await update.message.reply_text(f' به قند بات خوش آمدید , با /config  و وارد کردن config خود پس از ان, از مدت زمان حجم و config جدید در صورت تغیرات در سرور مطلع شوید. در صورت هرگونه مشکل با ghand_sup@  در ارتباط باشد ')
        await update.message.reply_photo(photo=image,)    
        
    async def get_details_by_config(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        config_uri=update.message.text.replace("/config","").replace(" ","")
        formatter=self.config_service.find_config_by_uri(config_uri)
        details=formatter.send_config_details()
        for msg in details:
            await update.message.reply_text(msg)
        await update.message.reply_text("کانفیگ ها هر ساعت یک بار به روز رسانی میشوند ")
        request.post_request(url=self.telegram_api_url,body={"chat_id":self.chat_id,"text":f'{formatter.config_name()} checked the config'})
            
    async def get_details_by_name(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context._chat_id == 6132337496:        
            config_remark=update.message.text.replace("/name","").replace(" ","")
            details=self.config_service.find_config_by_remark(config_remark).send_config_details()
            for msg in details:
                await update.message.reply_text(msg)
        else:
            await update.message.reply_text("shoma dastresi be in feature nadarid !!!")
            
    async def update_configs(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context._chat_id == 6132337496:        
            self.config_service.update_configs()
            await update.message.reply_text("done!")
        else:
            await update.message.reply_text("shoma dastresi be in feature nadarid !!!")

    async def config_message_handler(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "vmess://" in update.message.text or "vless://" in update.message.text :
                formater=self.config_service.find_config_by_uri(update.message.text)
                details=formater.send_config_details()
                for msg in details:
                    await update.message.reply_text(msg)
                await update.message.reply_text("کانفیگ ها هر ساعت یک بار به روز رسانی میشوند ")
                request.post_request(url=self.telegram_api_url,body={"chat_id":self.chat_id,"text":f'{formater.config_name()} checked the config'})
        else :
            await update.message.reply_text("کانفیگ را به صورت زیر وارد کنید ")
            await update.message.reply_text("/config vmess://eyh....")
        
            
            
    
def run_telegram_bot(config_service,telegram_api_url,chat_id,telegram_token):
    print("it is called and running telegram bot ")
    bot=Telegram_Bot(config_service,telegram_api_url,chat_id)
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start",bot.start))
    app.add_handler(CommandHandler("config",bot.get_details_by_config))
    app.add_handler(CommandHandler("name",bot.get_details_by_name))
    app.add_handler(CommandHandler("update",bot.update_configs))
    app.add_handler(MessageHandler(filters.TEXT,bot.config_message_handler))
    app.run_polling()




