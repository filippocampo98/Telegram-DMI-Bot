# -*- coding: utf-8 -*-
import requests
import bs4
import xlrd
import datetime
import sqlite3
import logging
from os.path import exists, join
from collections import OrderedDict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Unauthorized

logger = logging.getLogger(__name__)

def scrap(bot,job):

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
    nome_menu = menu.text;
    link_menu = menu.get("href")

    nome_file = nome_menu.lower()
    nome_file = nome_file.replace('ù', 'u')
    nome_file = nome_file.replace("menu",'')
    nome_file = nome_file.replace(' ','') + ".xls"

    if (not exists(join(PATH,nome_file))): # not =  !
        #Il file non esiste, crealo
        result = requests.get(link_menu, headers=headers)
        f = open(PATH+nome_file, "wb")
        f1 = open(PATH+"mensa.xls","wb")
        f.write(result.content)
        f1.write(result.content)

def mensa_get_menu():
    wb = xlrd.open_workbook("data/mensa.xls")
    sh = wb.sheet_by_index(0)
    #Week menu
    weekx =  (2,8,14,21,28,35,41)
    weeky = (6,12,18,25,32,39,45)
    rprimi = range(weekx[datetime.date.today().weekday()] , weeky[datetime.date.today().weekday()])
    rsecont = range(weekx[datetime.date.today().weekday()], weeky[datetime.date.today().weekday()] + 1)
    return wb, sh, weekx, weeky, rprimi, rsecont

def mensa(bot,update):
	wb, sh, weekx, weeky, rprimi, rsecont = mensa_get_menu()
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

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)

    if conn.execute("SELECT chatid FROM subscriptions WHERE chatid = " + str(chat_id)).fetchone():
        conn.execute("UPDATE 'subscriptions' SET `mensa`={} WHERE `chatid`={};".format(flag_mensa, chat_id))
    else:
        conn.execute("INSERT INTO 'subscriptions' (`chatid`, `mensa`) VALUES ({}, {});".format(chat_id, flag_mensa))
    conn.commit()

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

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)

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
    bot.editMessageText(chat_id=chat_id, text=message_text, message_id=update.callback_query.message.message_id)

def mensa_notify_lunch(bot, update):
    wb, sh, weekx, weeky, rprimi, rsecont = mensa_get_menu()
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

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)

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

def mensa_notify_dinner(bot, update):
    wb, sh, weekx, weeky, rprimi, rsecont = mensa_get_menu()

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

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)
    for row in conn.execute("SELECT chatid FROM subscriptions WHERE mensa = {} OR mensa = {} OR mensa = {} OR mensa = {}".format(x, y, x+3, y+3)):
    	try:
            bot.sendMessage(chat_id=row[0], text="🍽" + ind + messagep+ "\n" + messages + "\n" + messagec)
    	except Unauthorized:
    		logger.error('Unauthorized id. Trying to remove from the chat_id list from subscriptions')
    	except Exception as error:
    		open("logs/errors.txt", "a+").write(str(error)+" "+str(row[0])+"\n")
