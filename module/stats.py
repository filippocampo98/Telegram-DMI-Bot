# Telegram
from telegram import Update
from telegram.ext import CallbackContext

# System libraries
import sqlite3
from datetime import date, timedelta

def stats(update: Update, context: CallbackContext):
    if context.args:
        days = int(context.args[0])
        if days <= 0:
            days = 30
    else:
        days = 30
    stats_gen(update, context, days)

def stats_gen(update: Update, context: CallbackContext, days):
    conn = sqlite3.connect('data/DMI_DB.db')
    chat_id = update.message.chat_id
    text = ""

    if days == 0:
        text += "Record Globale:\n"
        query = "SELECT Type, n FROM (SELECT Type, COUNT(chat_id) as n FROM stat_list GROUP BY Type) ORDER BY n DESC;"
    else:
        text += "Record di "+str(days)+" giorni:\n"
        query = "SELECT Type, n FROM (SELECT Type, COUNT(chat_id) as n FROM stat_list WHERE DateCommand > '"+ str(date.today()-timedelta(days=days)) + "' GROUP BY Type) ORDER BY n DESC;"

    total = 0
    n_commands = 0
    for row in conn.execute(query):
        if str(row[0]) not in ("leiCheNePensaSignorina", "smonta_portoni", "santino", "bladrim", "prof_sticker"):
            text += f"{row[1]} : {row[0]}\n"
            total+= row[1]
            n_commands += 1
    text += f"\nTotale: {total}\nMedia per comando: {round(total/n_commands, 2)}"

    context.bot.sendMessage(chat_id=chat_id, text=text)
    conn.close()

def stats_tot(update: Update, context: CallbackContext):
    stats_gen(update, context, 0)