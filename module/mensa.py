# encoding=utf8
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
    except IndexError, ValueError:
        print "Errore mensa"
    nome_menu = menu.text;
    link_menu = menu.get("href")

    nome_file = nome_menu.lower().encode('utf-8').replace('ù', 'u').replace("menu",'').replace(' ','')+".xls"

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
	if(datetime.datetime.hour < 15):
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
		messagep += sh.cell(count,cprimi).value
		messagep += "\n"
	#Secondi
	for count in rsecont:
		messages += sh.cell(count,csecondi).value
		messages += "\n"
	#Contorni
	for count in rsecont:
		messagec += sh.cell(count,ccontorni).value
		messagec += "\n"

	bot.sendMessage(chat_id=update.message.chat_id, text = timemensa + "\n🍽" + ind + messagep+ "\n" + messages + "\n" + messagec)

def mensa_plus(bot, update):
	chat_id = update.message.chat_id
	keyboard=[[]]
	messageText="Scegli un'opzione per ricevere giornalmente il menu della mensa:"

	keyboard.append(
		[
			InlineKeyboardButton("Pranzo",           callback_data="mensa_pranzo"),
			InlineKeyboardButton("Pranzo e cena)",   callback_data="mensa_pranzo_cena")
		]
	)
	keyboard.append(
		[
			InlineKeyboardButton("Cena",             callback_data="mensa_cena"),
			InlineKeyboardButton("Disabilita",       callback_data="mensa_disabilita")
		]
	)
	reply_markup=InlineKeyboardMarkup(keyboard)
	bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=reply_markup)

def mensa_subscription(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    data = query.data

    flag_mensa = 0
    if data == "mensa_pranzo": flag_mensa=1
    elif data == "mensa_pranzo_cena": flag_mensa=2
    elif data == "mensa_cena": flag_mensa=3

    if flag_mensa == 0:
        message_text = "Notifiche disabilitate!"
    else:
        message_text = "Notifiche abilitate!"

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)

    flag = 0
    for row in conn.execute("SELECT chatid FROM subscriptions"):
        if row[0] == chat_id:
            flag=1

    if flag == 0:
        conn.execute("INSERT INTO 'subscriptions' (`chatid`, `mensa`) VALUES ({}, {});".format(chat_id, flag_mensa))
    else:
        conn.execute("UPDATE 'subscriptions' SET `mensa`={} WHERE `chatid`={};".format(flag_mensa, chat_id))
    conn.commit()

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
        messagep += sh.cell(count,cprimi).value
        messagep += "\n"
	#Secondi
    for count in rsecont:
        messages += sh.cell(count,csecondi).value
        messages += "\n"
	#Contorni
    for count in rsecont:
        messagec += sh.cell(count,ccontorni).value
        messagec += "\n"

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)
    for row in conn.execute("SELECT chatid FROM subscriptions WHERE mensa = 1 OR mensa == 2"):
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
        messagep += sh.cell(count,cprimi).value
        messagep += "\n"
    #Secondi
    for count in rsecont:
        messages += sh.cell(count,csecondi).value
        messages += "\n"
    #Contorni
    for count in rsecont:
        messagec += sh.cell(count,ccontorni).value
        messagec += "\n"

    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)
    for row in conn.execute("SELECT chatid FROM subscriptions WHERE mensa = 2 OR mensa == 3"):
    	try:
            bot.sendMessage(chat_id=row[0], text="🍽" + ind + messagep+ "\n" + messages + "\n" + messagec)
    	except Unauthorized:
    		logger.error('Unauthorized id. Trying to remove from the chat_id list from subscriptions')
    	except Exception as error:
    		open("logs/errors.txt", "a+").write(str(error)+" "+str(row[0])+"\n")
