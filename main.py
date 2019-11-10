import telegram, logging, threading, datetime

import modules.pytg.managers.config_manager as config_manager

import modules.pytg.handlers.messages_handler as pytg_messages_handler
import modules.pytg.handlers.callback_handler as pytg_callback_handler

# Ideally, your bot should want to implements all those components
import modules.dmibot.handlers.callback_handler as callback_handler
import modules.dmibot.handlers.commands_handler as commands_handler
import modules.dmibot.handlers.digest_handler as digest_handler
import modules.dmibot.handlers.jobs_handler as jobs_handler

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters 

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("dmibot.logs"),
            logging.StreamHandler()
        ]
    )

    # Start bot
    logging.info(" ### Launching Telegram DMI Bot... ### ")
    logging.info(str(datetime.datetime.now()))

    settings = config_manager.load_settings_file()

    bot = telegram.Bot(settings["token"])

    updater = Updater(settings["token"], use_context=True)
    dispatcher = updater.dispatcher

    # Your bot modules 
    commands_handler.load_command_handlers(dispatcher)
    callback_handler.load_callback_handlers(dispatcher)

    jobs_handler.schedule_jobs(updater.job_queue)
    digest_handler.load_digesters()

    # PyTG boilerplate
    pytg_callback_handler.load_callback_handlers(dispatcher)
    pytg_messages_handler.load_messages_handlers(dispatcher)

    # Start polling
    updater.start_polling()
    logging.info("Polling.")

if __name__ == '__main__':
    main()
