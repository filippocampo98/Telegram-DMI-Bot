import telegram, yaml, logging

from telegram.ext import CallbackQueryHandler

from modules.dmibot.handlers.callback.mdmsg import mdmsg_callback_handler
from modules.dmibot.handlers.callback.menu_cmd import menu_cmd_callback_handler

def load_callback_handlers(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(mdmsg_callback_handler, pattern="mdmsg,.*"))
    dispatcher.add_handler(CallbackQueryHandler(menu_cmd_callback_handler, pattern="menu_cmd,.*"))
