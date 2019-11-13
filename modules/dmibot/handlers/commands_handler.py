import telegram, yaml, logging

from telegram.ext import CommandHandler

from modules.dmibot.handlers.commands.start import start_cmd_handler
from modules.dmibot.handlers.commands.help import help_cmd_handler
from modules.dmibot.handlers.commands.esami import esami_cmd_handler

def load_command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start_cmd_handler))
    dispatcher.add_handler(CommandHandler("help", help_cmd_handler))
    dispatcher.add_handler(CommandHandler("esami", esami_cmd_handler, pass_args=True))

