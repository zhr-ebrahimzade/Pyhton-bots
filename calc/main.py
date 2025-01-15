from typing import Final

from telegram import Update
import telegram.ext


BOT_TOKEN: Final = "**************************"


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def add_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    a=int(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"{a[0]} + {a[1]} = {a[0]+a[a]}")


async def multiplication_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    # write your code here
    pass


async def calculate_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # write your code here
    pass


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))
    # add all your handlers here
    bot.add_handler(CommandHandler("add", add_command_handler()))

    # start bot
    bot.run_polling()
