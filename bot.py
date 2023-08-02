from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from server_class import Server



turkey=Server(server_ip="130.0.237.194",server_port=13713,username="mahan",password="mahan",config_url="hello.com")
turkey.get_configs().json()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'turkey.get_configs().json()')


app = ApplicationBuilder().token("6372238157:AAFesiFi15vJC7EaBveXqImnpBCbVyWxB50").build()

app.add_handler(CommandHandler("get_all_config", hello))

app.run_polling()