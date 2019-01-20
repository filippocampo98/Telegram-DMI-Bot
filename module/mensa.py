# -*- coding: utf-8 -*-
import requests
import bs4
import xlrd
import datetime
import sqlite3
import logging
import yaml
import os
from os.path import exists, join
from collections import OrderedDict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Unauthorized

logger = logging.getLogger(__name__)

with open('config/settings.yaml', 'r') as yaml_config:
    config_map = yaml.load(yaml_config)

def handle_scrape(bot, job):

    if exists('data/mensa.xls'):
        _, __, ___, firstdate, secondate = mensa_get_menu()
        if not (firstdate <= datetime.datetime.now() <= secondate):
            os.remove("data/mensa.xls")
            scrape(bot, job)
    else:
        scrape(bot,job)

def scrape(bot,job):

    url = "http://www.ersucatania.gov.it/menu-mensa/"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    result = requests.get(url, headers=headers).content
    PATH = "data/"

    SECTION_ = "section"
    CLASS_ = "entry-content clearfix"

    soup = bs4.BeautifulSoup(result, "html.parser")

    try:
        menu = soup.find(SECTION_, class_= CLASS_).find_all("p")[1].find("a") # Contiene nome Menu
    except (IndexError, ValueError):
        print ("Errore mensa")

    nome_menu = menu.text
    link_menu = menu.get("href")

    nome_file = nome_menu.lower()
    nome_file = nome_file.replace('ù', 'u')
    nome_file = nome_file.replace("menu",'')
    nome_file = nome_file.replace(' ','') + ".xls"
    nome_file = nome_file.replace("/",".")

    if (not exists(join(PATH,nome_file))):
        # se il file non esiste, crealo
        result = requests.get(link_menu, headers=headers)

        f = open(PATH+nome_file, "wb")
        f.write(result.content)
        f.close()

        sh, _, __, firstdate, secondate = mensa_get_menu(PATH+nome_file)

        if (firstdate <= datetime.datetime.now() <= secondate):
            f1 = open(PATH+"mensa.xls","wb")
            f1.write(result.content)
            f1.close()
    
    if exists("data/mensa.xls"):
        os.system("mv data/mensa.xls data/mensa.xls.keep && rm data/*.xls && mv data/mensa.xls.keep data/mensa.xls")
    else:
        os.system("rm data/*.xls")
    
    logger.info("Menù Mensa loaded.")

def mensa_get_menu(mensa_file="data/mensa.xls"):
    wb = xlrd.open_workbook(mensa_file)
    sh = wb.sheet_by_index(0)

    mensa_date = sh.cell(0,3).value.lower()
    mensa_date = mensa_date.replace("dal", "")
    mensa_date = mensa_date.replace("al", "")
    mensa_date = mensa_date.strip() # trim
    mensa_date = mensa_date.replace("  ", " ")
    mensa_date = mensa_date.replace("/19", "/2019")
    mensa_date = mensa_date.split(" ")

    #Week range
    firstdate = datetime.datetime.strptime(mensa_date[0],"%d/%m/%Y")
    secondate = datetime.datetime.strptime(mensa_date[1],"%d/%m/%Y")

    #Week menu
    weekx =  (2,8,14,21,28,35,41)
    weeky = (6,12,18,25,32,39,45)
    rprimi = range(weekx[datetime.date.today().weekday()] , weeky[datetime.date.today().weekday()] + 1)
    rsecont = range(weekx[datetime.date.today().weekday()], weeky[datetime.date.today().weekday()] + 1)
    return sh, rprimi, rsecont, firstdate, secondate

def mensa(bot,update):
    sh, rprimi, rsecont, firstdate, secondate = mensa_get_menu()

    if not(firstdate.date() <= datetime.datetime.now().date() <= secondate.date()):
        bot.sendMessage(chat_id=update.message.chat_id, text = "⚠️ Menù mensa non disponibile!")
    else:
        if(datetime.datetime.now().hour < 15):
            cprimi = 1
            csecondi = 3
            ccontorni = 5
            ind =  "MENÙ PRANZO: %d/%d/%d \n" % (datetime.datetime.now().day, datetime.datetime.now().month,datetime.datetime.now().year)
        else:
            cprimi = 7
            csecondi = 9
            ccontorni = 11
            ind = "MENÙ CENA: %d/%d/%d \n" % (datetime.datetime.now().day, datetime.datetime.now().month,datetime.datetime.now().year)
        messagep = ""
        messages = ""
        messagec = ""
        #Orari mensa
        timemensa = "🕑 Orario Mensa \nPranzo dalle ore 12,15 alle ore 14,30 \nCena dalle ore 19,00 alle ore 21,30 \n "
        #Primi
        for count in rprimi:
            if count < sh.nrows:
                messagep += sh.cell(count,cprimi).value
            messagep += "\n"
        #Secondi
        for count in rsecont:
            if count < sh.nrows:
                messages += sh.cell(count,csecondi).value
            messages += "\n"
        #Contorni
        for count in rsecont:
            if count < sh.nrows:
                messagec += sh.cell(count,ccontorni).value
            messagec += "\n"

        bot.sendMessage(chat_id=update.message.chat_id, text = timemensa + "\n🍽" + ind + messagep+ "\n" + messages + "\n" + messagec)



def mensa_plus(bot, update):
	chat_id = update.message.chat_id
	keyboard=[[]]
	message_text="Scegli un'opzione per ricevere giornalmente il menu della mensa:"

	keyboard.append(
		[
			InlineKeyboardButton("Pranzo",           callback_data="mensa_pranzo"),
			InlineKeyboardButton("Pranzo e cena",    callback_data="mensa_pranzo_cena")
		]
	)
	keyboard.append(
		[
			InlineKeyboardButton("Cena",             callback_data="mensa_cena"),
			InlineKeyboardButton("Disabilita",       callback_data="mensa_disabilita")
		]
	)
	reply_markup=InlineKeyboardMarkup(keyboard)
	bot.sendMessage(chat_id=chat_id, text=message_text, reply_markup=reply_markup)

def mensa_subscription(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    data = query.data

    flag_mensa = 0
    message_text = "Notifiche disabilitate!"

    if data == "mensa_pranzo":
        flag_mensa = 1
        message_text = "Notifiche abilitate! Da ora in avanti riceverai alle 11:45 il menu del pranzo."
    elif data == "mensa_pranzo_cena":
        flag_mensa = 2
        message_text = "Notifiche abilitate! Da ora in avanti riceverai alle 11:45 il menu del pranzo ed alle 18:45 il menu della cena."
    elif data == "mensa_cena":
        flag_mensa = 3
        message_text = "Notifiche abilitate! Da ora in avanti riceverai alle 18:45 il menu della cena."

    conn = sqlite3.connect('data/DMI_DB.db')

    if conn.execute("SELECT chatid FROM subscriptions WHERE chatid = " + str(chat_id)).fetchone():
        conn.execute("UPDATE 'subscriptions' SET `mensa`={} WHERE `chatid`={};".format(flag_mensa, chat_id))
    else:
        conn.execute("INSERT INTO 'subscriptions' (`chatid`, `mensa`) VALUES ({}, {});".format(chat_id, flag_mensa))
    conn.commit()
    conn.close()

    if flag_mensa != 0:
        keyboard = [[]]
        message_text += "\n Abilita o disabilita le notifiche nel weekend:"

        keyboard.append(
            [
                InlineKeyboardButton("Abilita nel Weekend",     callback_data="mensa_weekend"),
                InlineKeyboardButton("Disabilita nel Weekend",  callback_data="mensa_weekend_no")
            ]
        )
        reply_markup=InlineKeyboardMarkup(keyboard)
        bot.editMessageText(chat_id=chat_id, text=message_text, message_id=update.callback_query.message.message_id, reply_markup=reply_markup)
    else:
        bot.editMessageText(chat_id=chat_id, text=message_text, message_id=update.callback_query.message.message_id)

def mensa_weekend(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    data = query.data

    conn = sqlite3.connect('data/DMI_DB.db')

    mensa = conn.execute("SELECT mensa FROM subscriptions WHERE chatid=%s"% chat_id).fetchone()[0]

    if data == "mensa_weekend_no":
        if mensa > 3:
            mensa -= 3
        message_text = "Notifiche disabilitate nel weekend!"
        conn.execute("UPDATE 'subscriptions' SET `mensa`={} WHERE `chatid`={};".format(mensa, chat_id))
    else:
        if mensa <= 3:
            mensa += 3
        message_text = "Notifiche abilitate nel weekend!"
        conn.execute("UPDATE 'subscriptions' SET `mensa`={} WHERE `chatid`={};".format(mensa, chat_id))
    conn.commit()
    conn.close()
    bot.editMessageText(chat_id=chat_id, text=message_text, message_id=update.callback_query.message.message_id)

def mensa_notify_lunch(bot, update):
    sh, rprimi, rsecont, firstdate, secondate = mensa_get_menu()

    if (firstdate.date() <= datetime.datetime.now().date() <= secondate.date()):
        cprimi = 1
        csecondi = 3
        ccontorni = 5
        ind =  "MENÙ PRANZO: %d/%d/%d \n" % (datetime.datetime.now().day, datetime.datetime.now().month,datetime.datetime.now().year)

        messagep = ""
        messages = ""
        messagec = ""

        #Primi
        for count in rprimi:
            if count < sh.nrows:
                messagep += sh.cell(count,cprimi).value
            messagep += "\n"
        #Secondi
        for count in rsecont:
            if count < sh.nrows:
                messages += sh.cell(count,csecondi).value
            messages += "\n"
        #Contorni
        for count in rsecont:
            if count < sh.nrows:
                messagec += sh.cell(count,ccontorni).value
            messagec += "\n"

        conn = sqlite3.connect('data/DMI_DB.db')

        x = 1
        y = 2
        if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6:
            x += 3
            y += 3

        for row in conn.execute("SELECT chatid FROM subscriptions WHERE mensa = {} OR mensa = {} OR mensa = {} OR mensa = {}".format(x, y, x+3, y+3)):
            try:
                bot.sendMessage(chat_id=row[0], text="🍽 " + ind + messagep+ "\n" + messages + "\n" + messagec)
            except Unauthorized:
                logger.error('Unauthorized id. Trying to remove from the chat_id list from subscriptions')
            except Exception as error:
                open("logs/errors.txt", "a+").write(str(error)+" "+str(row[0])+"\n")
        conn.close()

        if config_map['mensa_channel'] != "@channelusername":
            try:
                bot.sendMessage(chat_id=config_map['mensa_channel'], text="🍽 " + ind + messagep+ "\n" + messages + "\n" + messagec + "\n Powered by @DMI_Bot", parse_mode='HTML')
            except Exception as error:
                open("logs/errors.txt", "a+").write("{} {}\n".format(error, config_map['mensa_channel']))

def mensa_notify_dinner(bot, update):
    sh, rprimi, rsecont, firstdate, secondate = mensa_get_menu()

    if (firstdate.date() <= datetime.datetime.now().date() <= secondate.date()):
        cprimi = 7
        csecondi = 9
        ccontorni = 11
        ind = "MENÙ CENA: %d/%d/%d \n" % (datetime.datetime.now().day, datetime.datetime.now().month,datetime.datetime.now().year)
        messagep = ""
        messages = ""
        messagec = ""
        #Primi
        for count in rprimi:
            if count < sh.nrows:
                messagep += sh.cell(count,cprimi).value
            messagep += "\n"
        #Secondi
        for count in rsecont:
            if count < sh.nrows:
                messages += sh.cell(count,csecondi).value
            messages += "\n"
        #Contorni
        for count in rsecont:
            if count < sh.nrows:
                messagec += sh.cell(count,ccontorni).value
            messagec += "\n"

        x = 2
        y = 3
        if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6:
            x += 3
            y += 3

        conn = sqlite3.connect('data/DMI_DB.db')
        for row in conn.execute("SELECT chatid FROM subscriptions WHERE mensa = {} OR mensa = {} OR mensa = {} OR mensa = {}".format(x, y, x+3, y+3)):
            try:
                bot.sendMessage(chat_id=row[0], text="🍽" + ind + messagep+ "\n" + messages + "\n" + messagec)
            except Unauthorized:
                logger.error('Unauthorized id. Trying to remove from the chat_id list from subscriptions')
            except Exception as error:
                open("logs/errors.txt", "a+").write(str(error)+" "+str(row[0])+"\n")
        conn.close()

        if config_map['mensa_channel'] != "@channelusername":
            try:
                bot.sendMessage(chat_id=config_map['mensa_channel'], text="🍽" + ind + messagep+ "\n" + messages + "\n" + messagec + "\n Powered by @DMI_Bot", parse_mode='HTML')
            except Exception as error:
                open("logs/errors.txt", "a+").write("{} {}\n".format(error, config_map['mensa_channel']))
