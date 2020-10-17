from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import random

from module.shared import check_log, CUSicon

def help_cmd():
    output = "@DMI_Bot risponde ai seguenti comandi: \n\n"
    output += "📖 /esami - linka il calendario degli esami\n"
    output += "🗓 /aulario - linka l\'aulario\n"
    output += "👔 /prof <nome> - es. /prof Barbanera\n"
    output += "👥 /rappresentanti - elenco dei rappresentanti del DMI\n"
    output += "📚 /biblioteca - orario biblioteca DMI\n"
    output += CUSicon[random.randint(0, 5)] + " /cus sede e contatti\n"
    output += "  /cloud - linka le cartelle condivise su cloud\n\n"
    output += "Segreteria orari e contatti:\n"
    output += "/sdidattica - segreteria didattica\n"
    output += "/sstudenti - segreteria studenti\n"
    output += "/cea - CEA\n"
    output += "\nERSU orari e contatti\n"
    output += "/ersu - sede centrale\n"
    output += "/ufficioersu - (ufficio tesserini)\n"
    output += "/urp - URP studenti\n\n"
    output += "~Bot~\n"
    output += "📂 /drive - accedi a drive\n"
    output += "📂 /git - /gitlab - accedi a gitlab\n"
    output += "/contributors"
    output += "/regolamentodidattico"
    return output

def help(update: Update, context: CallbackContext):
    check_log(update, context, "help")
    chat_id = update.message.chat_id
    keyboard = [[]]
    message_text = "@DMI_Bot risponde ai seguenti comandi:"

    keyboard.append([InlineKeyboardButton(" ~ Dipartimento e CdL ~ ", callback_data="_div")])

    keyboard.append(
        [
            InlineKeyboardButton("📖 Esami (link)",        callback_data="md_esami_link"),
            InlineKeyboardButton("🗓 Aulario",              url='http://aule.dmi.unict.it/booked/Web/view-schedule.php'),
            InlineKeyboardButton("Orari lezioni (link)",    callback_data="md_lezioni_link")
        ]
    )

    keyboard.append(
        [InlineKeyboardButton("Regolamento Didattico", callback_data="regolamentodidattico_button")]
    )

    keyboard.append(
        [
            InlineKeyboardButton("👥 Rappresentanti",                       callback_data="sm_rapp_menu"),
            InlineKeyboardButton("📚 Biblioteca",                           callback_data="md_biblioteca"),
            InlineKeyboardButton(CUSicon[random.randint(0, 5)] + " CUS",    callback_data="md_cus"),
            InlineKeyboardButton("☁️ Cloud",                                 callback_data="md_cloud")
        ]
    )

    keyboard.append([InlineKeyboardButton(" ~ Segreteria orari e contatti ~ ", callback_data="_div")])

    keyboard.append(
        [
            InlineKeyboardButton("Seg. Didattica",  callback_data="md_sdidattica"),
            InlineKeyboardButton("Seg. Studenti",   callback_data="md_sstudenti"),
            InlineKeyboardButton("CEA",             callback_data="md_cea")
        ]
    )

    keyboard.append([InlineKeyboardButton(" ~ ERSU orari e contatti ~ ", callback_data="_div")])

    keyboard.append(
        [
            InlineKeyboardButton("ERSU",          callback_data="md_ersu"),
            InlineKeyboardButton("Ufficio ERSU",  callback_data="md_ufficioersu"),
            InlineKeyboardButton("URP",           callback_data="md_urp")
        ]
    )

    keyboard.append([InlineKeyboardButton(" ~ Bot e varie ~ ", callback_data="_div")])

    keyboard.append(
        [
            InlineKeyboardButton("📂 Drive",     callback_data="md_drive"),
            InlineKeyboardButton("📂 GitLab",    callback_data="md_gitlab"),
            InlineKeyboardButton("Contributors", callback_data="md_contributors"),
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton("Tutti i comandi", callback_data="help_cmd"),
            InlineKeyboardButton("Chiudi",          callback_data="exit_cmd")
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.sendMessage(chat_id=chat_id, text=message_text, reply_markup=reply_markup)

def rapp_menu(update: Update, context: CallbackContext, chat_id, message_id):
    keyboard = [[]]
    message_text = "Quali rappresentanti vuoi contattare?"

    keyboard.append(
        [
            InlineKeyboardButton("Rapp. DMI",         callback_data="md_rappresentanti_dmi"),
            InlineKeyboardButton("Rapp. Informatica", callback_data="md_rappresentanti_informatica"),
            InlineKeyboardButton("Rapp. Matematica",  callback_data="md_rappresentanti_matematica"),
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.editMessageText(text=message_text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)

def exit_cmd():
    output = "."
    return output