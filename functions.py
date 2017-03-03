# -*- coding: utf-8 -*-
#Telegram
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, RegexHandler

#Drive
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# custom classes
from classes.StringParser import StringParser

# system libraries
from datetime import date, datetime, timedelta
import json,datetime,re,random,os,sys
import requests
import urllib2
from bs4 import BeautifulSoup
import sqlite3
import logging

from pprint import pprint
from sets import Set
import calendar
import locale
import time

locale.setlocale(locale.LC_ALL, 'it_IT.utf8')

# debug
disable_chatid_logs = 1 #news, stats
disable_db = 1          #stats, drive
disable_drive = 1       #drive

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)

#token
tokenconf = open('config/token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf      		#Token of your telegram bot that you created from @BotFather, write it on token.conf

def output_lezioni(item):
    daylist = list(calendar.day_name)
    output = ""

    output += "*Insegnamento:* " + item["insegnamento"]
    output += "\n*Aula:* " + item["aula"]
    for day in daylist:
        if(day.replace('ì','i') in item and item[day.replace('ì','i')] != ""):
            output += "\n*" + day.title() + ":* " + item[day.replace('ì','i')]
    output += "\n*Anno:* " + item["anno"] + "\n"

    return output

def condition_lezioni(items, condition, *arg):
    output = Set()
    for item in items:
        if(arg):
            if(arg[0] in item[condition].lower()):
                output.add(output_lezioni(item))
        else:
            if(condition.replace('ì','i') in item and item[condition.replace('ì','i')] != ""):
                output.add(output_lezioni(item))

    return output

def condition_mult_lezioni(items, days, years):
    output = Set()
    for item in items:
        for day in days:
            if( [year for year in years if year in item["anno"].lower()] ):
                if(day.replace('ì','i') in item and item[day.replace('ì','i')] != ""):
                    output.add(output_lezioni(item))
    return output

def lezioni_cmd(args):
    output = Set()
    r = requests.get('http://localhost/PHP-DMI-API/result/lezioni_dmi.json')
    if(r.status_code == requests.codes.ok):

        items = r.json()["items"]
        daylist = list(calendar.day_name)

        args = [x.lower().encode('utf-8') for x in args if len(x) > 2]
        if 'anno' in args: args.remove('anno')

        if(len(args) == 1):

            if(args[0] in daylist):
                output = condition_lezioni(items, args[0])

            elif(args[0] == "oggi"):
                output = condition_lezioni(items, time.strftime("%A"))

            elif(args[0] == "domani"):
                tomorrow_date = datetime.datetime.today() + datetime.timedelta(1)
                tomorrow_name = datetime.datetime.strftime(tomorrow_date,'%A')
                output = condition_lezioni(items, tomorrow_name)

            elif(args[0] in ("primo", "secondo", "terzo")):
                output = condition_lezioni(items, "anno", args[0])

            elif([item["insegnamento"].lower().find(args[0]) for item in items]):
                output = condition_lezioni(items, "insegnamento", args[0])

            if(len(output)):
                string = '\n'.join(list(output))
                string += "\n_Ultimo aggiornamento: " + r.json()["status"]["lastupdate"] + "_\n"
            else:
                string = "Nessun risultato trovato :(\n"
        elif(len(args) > 1):

            days = list(set(args).intersection(daylist))
            years = list(set(args).intersection(("primo", "secondo", "terzo")))

            if(days and years):
                output = condition_mult_lezioni(items, days, years)

            elif("oggi" in args and years):
                days = [time.strftime("%A")]
                output = condition_mult_lezioni(items, days, years)

            elif("domani" in args and years):
                tomorrow_date = datetime.datetime.today() + datetime.timedelta(1)
                tomorrow_name = datetime.datetime.strftime(tomorrow_date,'%A')
                days = [tomorrow_name]
                output = condition_mult_lezioni(items, days, years)

            else:
                for arg in args:
                    output = output.union(condition_lezioni(items, "insegnamento", arg))

            if(len(output)):
                string = '\n'.join(list(output))
                string += "\n_Ultimo aggiornamento: " + r.json()["status"]["lastupdate"] + "_\n"
            else:
                string = "Nessun risultato trovato :(\n"
        else:
            string = "Inserisci almeno un parametro.\n"

    return string

def lezioni(bot, update, args):
    checkLog(bot, update, "lezioni")
    messageText = lezioni_cmd(args)
    bot.sendMessage(chat_id=update.message.chat_id, text=messageText, parse_mode='Markdown')

def getProfessori(input):
    with open("data/json/professori.json") as data_file:
        professori_data = json.load(data_file)

    output = ""
    i = 0

    while(professori_data[i]["ID"] != "-1"):
        if (input == "/prof"):
	    return "La sintassi del comando è: /prof <nomeprofessore>"
	if len(input) < 3:
            return "Inserisci almeno 3 caratteri come nome/cognome del professore"
        elif (( input.lower() in professori_data[i]["Nome"].lower() ) or ( input.lower() in professori_data[i]["Cognome"].lower() )):
            output += "Ruolo: " + professori_data[i]["Ruolo"] + "\n"
            output += "Cognome: " + professori_data[i]["Cognome"] + "\n"
            output += "Nome: " + professori_data[i]["Nome"] + "\n"
            output += "Indirizzo email : " + professori_data[i]["Email"] + "\n"
            output += "Sito web: " + professori_data[i]["Sito"] + "\n"
            output += "Scheda DMI: " + professori_data[i]["SchedaDMI"] + "\n\n"
        i += 1
    if output == "":
        return "\nNon sono stati trovati risultati :(\n\n"

    return output #Redefine with @TkdAlex

def forum(sezione):

    response = urllib2.urlopen("http://forum.informatica.unict.it/")
    html_doc = response.read()

    #print(html_doc)
    s = BeautifulSoup(html_doc, 'html.parser')
    s.prettify()
    dictionary = {}
    for rangeLimit,mainTable in enumerate(s.findAll("div", class_="tborder")):
        if(rangeLimit >= 3): #If che limita le sezioni a quelle interessate, evitando di stampare sottosezioni come "News" della categoria "Software"
            break
        for tdOfTable in mainTable.findAll("td", class_="windowbg3"):
            for spanUnder in tdOfTable.findAll("span", class_="smalltext"):
                for anchorTags in spanUnder.find_all('a'):
                    anchorTagsSplitted = anchorTags.string.split(",")
                    anchorTagsWithoutCFU = StringParser.removeCFU(anchorTagsSplitted[0])

                    if(sezione == anchorTagsWithoutCFU.lower()):
                        dictionary[anchorTagsWithoutCFU.lower()] = anchorTags['href']
                        return dictionary

    return False #Redefine with @Veeenz API

# Commands
CUSicon = {0 : "🏋",
	   1 : "⚽️",
	   2 : "🏀",
	   3 : "🏈",
	   4 : "🏐",
	   5 : "🏊",
}

def help_cmd():
    output = "@DMI_Bot risponde ai seguenti comandi: \n\n"
    output += "📖 /esami - /mesami - linka il calendario degli esami\n"
    output += "🗓 /aulario - linka l\'aulario\n"
    output += "👔 /prof <nome> - es. /prof Milici\n"
    output += "🍽 /mensa - orario mensa\n"
    output += "👥 /rappresentanti - elenco dei rappresentanti del DMI\n"
    output += "📚 /biblioteca - orario biblioteca DMI\n"
    output += CUSicon[random.randint(0,5)] + " /cus sede e contatti\n\n"
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
    output += "/disablenews \n"
    output += "/enablenews\n"
    output += "/contributors"
    return output

def contributors_cmd():
	output = "@Helias, @adriano_effe, @Veenz, @simone989\n"
	output +="https://github.com/UNICT-DMI/Telegram-DMI-Bot.git"
	return output

def contributors(bot, update):
	checkLog(bot, update, "contributors")
	messageText = contributors_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def read_md(namefile):
    in_file = open("data/markdown/" + namefile + ".md","r")
    text = in_file.read()
    in_file.close()
    return text

def custom_callback(bot, update, cmd):
    checkLog(bot, update, cmd)
    messageText = read_md(cmd)
    bot.sendMessage(chat_id=update.message.chat_id, text=messageText, parse_mode='Markdown')

def prof_cmd(text):
	text = text.replace("@dmi_bot", "")
	text = text.replace("/prof ", "")
	output = getProfessori(text)
	return output

def rapp_cmd():
	output = "Usa uno dei seguenti comandi per mostrare i rispettivi rappresentanti\n"
	output += "/rappresentanti_dmi\n"
	output += "/rappresentanti_informatica\n"
	output += "/rappresentanti_matematica"
	return output

def rapp_dmi_cmd():
	output =  "Rappresentanti DMI\n"
	output += "Aliperti Vincenzo - @VAliperti\n"
	output += "Apa Marco - @MarcoApa\n"
	output += "Borzì Stefano - @Helias\n"
	output += "Costa Alberto - @knstrct\n"
	output += "Marroccia Marco - @MarcoLebon\n"
	output += "Mattia Ferdinando Alessandro - @AlessandroMattia\n"
	output += "Presente Fabrizio\n"
	output += "Petralia Luca- @lucapppla\n"
	output += "Rapisarda Simone - @CarlinoMalvagio\n"
	output += "Ricordo che per segnalare qualcosa a tutti i rappresentanti si può utilizzare l'email reportdmiunict@gmail.com"
	return output

def rapp_inf_cmd():
	output =  "Rappresentanti Inforamtica\n"
	output += "Aliperti Vincenzo - @VAliperti\n"
	output += "Apa Marco - @MarcoApa\n"
	output += "Borzì Stefano - @Helias\n"
	output += "Costa Alberto - @knstrct\n"
	output += "Giangreco Antonio - @Antonio0793\n"
	output += "Marroccia Marco - @MarcoLebon\n"
	return output

def rapp_mat_cmd():
	output =  "Rappresentanti Matematica\n"
	output += "Alessandro Massimiliano - @massi_94\n"
	output += "De Cristofaro Gaetano\n"
	output += "Pratissoli Mirco - @Mirko291194\n"
	output += "Sciuto Rita - @RitaSciuto"
	return output

#Easter egg
def smonta_portoni_cmd():
	r = random.randint(0,13)
	if (r >= 0 and r <= 3):
		output = "$ sudo umount portoni"
	elif (r > 3 and r < 10):
		output = "@TkdAlex"
	elif (r == 11):
		output = "https://s16.postimg.org/5a6khjb5h/smonta_portoni.jpg"
	else:
		output = "https://s16.postimg.org/rz8117y9x/idraulico.jpg"
	return output

def santino_cmd():
    r = random.randint(0,20)
    if (r >= 0 and r <= 3):
        output = "@Santinol"
    elif (r > 3 and r < 10):
        output = "https://s18.postimg.org/t13s9lai1/photo_2016_11_24_11_04_42.jpg"
    elif (r >= 10 and r < 16):
		output = "https://s11.postimg.org/yiwugh4ib/photo_2016_11_24_11_04_31.jpg"
    elif (r >=16 and r < 21):
        output = "https://s12.postimg.org/5d7y88pj1/photo_2016_11_24_11_04_29.jpg"

    return output

def forum_cmd(text):
	text = text.replace("/forum ","")
	dictUrlSezioni = forum(text)
	if not (dictUrlSezioni == False):
		for titoli in dictUrlSezioni:
			output = StringParser.startsWithUpper(titoli)+": "+str(dictUrlSezioni[titoli])
	else:
		output = "La sezione non e' stata trovata."
	return output

def callback(bot, update):
	keyboard2=[[]];
	icona=""
	NumberRow=0
	NumberArray=0
	update_id = update.update_id

	if len(update.callback_query.data)<13:
		#conn.execute("DELETE FROM 'Chat_id_List'")
		ArrayValue=update['callback_query']['message']['text'].split(" ")
		try:
			if len(ArrayValue)==5:
				conn.execute("INSERT INTO 'Chat_id_List' VALUES ("+update.callback_query.data+",'"+ArrayValue[4]+"','"+ArrayValue[1]+"','"+ArrayValue[2]+"','"+ArrayValue[3]+"') ")
				bot.sendMessage(chat_id=update.callback_query.data,text= "🔓 La tua richiesta è stata accettata")
				bot.sendMessage(chat_id=-1001095167198,text=str(ArrayValue[1])+" "+str(ArrayValue[2]+str(" è stato inserito nel database")))

			elif len(ArrayValue)==4:
				conn.execute("INSERT INTO 'Chat_id_List'('Chat_id','Nome','Cognome','Email') VALUES ("+update.callback_query.data+",'"+ArrayValue[1]+"','"+ArrayValue[2]+"','"+ArrayValue[3]+"')")
				bot.sendMessage(chat_id=update.callback_query.data,text= "🔓 La tua richiesta è stata accettata")

			else:
				bot.sendMessage(chat_id=-1001095167198,text=str("ERRORE INSERIMENTO: ")+str(update['callback_query']['message']['text'])+" "+str(update['callback_query']['data']))
			conn.commit()
		except Exception as error:
			bot.sendMessage(chat_id=-1001095167198,text=str("ERRORE INSERIMENTO: ")+str(update['callback_query']['message']['text'])+" "+str(update['callback_query']['data']))




		LAST_UPDATE_ID = update_id + 1
		text = ""
		messageText = ""

	else:
		if(os.fork()==0):
			settings_file = "config/settings.yaml"
			gauth2 = GoogleAuth(settings_file=settings_file)
			gauth2.CommandLineAuth()
			#gauth2.LocalWebserverAuth()
			drive2 = GoogleDrive(gauth2)
			bot2 = telegram.Bot(TOKEN)

			file1=drive2.CreateFile({'id':update.callback_query.data})
			if file1['mimeType']=="application/vnd.google-apps.folder":
				file_list2= drive2.ListFile({'q': "'"+file1['id']+"' in parents and trashed=false",'orderBy':'folder,title'}).GetList()
				for file2 in file_list2:

					fileN=""

					if file2['mimeType']=="application/vnd.google-apps.folder":
						if NumberRow>=1:
							keyboard2.append([InlineKeyboardButton("🗂 "+file2['title'], callback_data=file2['id'])])
							NumberRow=0
							NumberArray+=1
						else:
							keyboard2[NumberArray].append(InlineKeyboardButton("🗂 "+file2['title'], callback_data=file2['id']))
							NumberRow+=1
					else:
						if  ".pdf" in file2['title']:
							icona="📕 "
						elif ".doc" in file2['title'] or ".docx" in file2['title'] or ".txt" in file2['title'] :
							icona="📘 "
						elif ".jpg" in file2['title'] or ".png" in file2['title'] or ".gif" in  file2['title']:
							icona="📷 "
						elif ".rar" in file2['title'] or ".zip" in file2['title']:
							icona="🗄 "
						elif ".out" in file2['title'] or ".exe" in file2['title']:
							icona="⚙ "
						elif ".c" in file2['title'] or ".cpp" in file2['title'] or ".py" in file2['title'] or ".java" in file2['title'] or ".js" in file2['title'] or ".html" in file2['title'] or ".php" in file2['title']:
							icona="💻 "
						else:
							icona="📄 "
						if NumberRow>=1:
							keyboard2.append([InlineKeyboardButton(icona+file2['title'], callback_data=file2['id'])])
							NumberRow=0
							NumberArray+=1
						else:
							keyboard2[NumberArray].append(InlineKeyboardButton(icona+file2['title'], callback_data=file2['id']))
							NumberRow+=1

				if file1['parents'][0]['id'] != '0ADXK_Yx5406vUk9PVA':
					keyboard2.append([InlineKeyboardButton("🔙", callback_data=file1['parents'][0]['id'])])
				reply_markup3 = InlineKeyboardMarkup(keyboard2)
				bot2.sendMessage(chat_id=update['callback_query']['from_user']['id'],text=file1['title']+":", reply_markup=reply_markup3)

			elif file1['mimeType'] == "application/vnd.google-apps.document":
				bot2.sendMessage(chat_id=update['callback_query']['from_user']['id'], text="Impossibile scaricare questo file poichè esso è un google document, Andare sul seguente link")
				bot2.sendMessage(chat_id=update['callback_query']['from_user']['id'], text=file1['exportLinks']['application/pdf'])

			else:
				try:
					fileD=drive2.CreateFile({'id':file1['id']})
					if int(fileD['fileSize']) < 5e+7:
						fileD.GetContentFile('file/'+file1['title'])
						fileS=file1['title']
						filex=open(str("file/"+fileS),"rb")
						bot2.sendChatAction(chat_id=update['callback_query']['from_user']['id'], action="UPLOAD_DOCUMENT")
						bot2.sendDocument(chat_id=update['callback_query']['from_user']['id'], document=filex)
						os.remove(str("file/"+fileS))
					else:
						bot2.sendMessage(chat_id=update['callback_query']['from_user']['id'], text="File troppo grande per il download diretto, scarica dal seguente link")
						bot2.sendMessage(chat_id=update['callback_query']['from_user']['id'],text=fileD['alternateLink']) ##fileD['downloadUrl']
				except Exception as e:
					print str(e)
					bot2.sendMessage(chat_id=update['callback_query']['from_user']['id'],text="Impossibile scaricare questo file, contattare gli sviluppatori del bot")
					open("logs/errors.txt","a+").write(str(e)+str(fileD['title'])+"\n")

			sys.exit(0)

def request(bot, update):
	chat_id = update.message.chat_id
	flag=0
	if (chat_id>0):
		for row in conn.execute("SELECT Chat_id FROM Chat_id_List"):
			if row[0] == chat_id:
				flag=1

		if flag==0:
			messageText="✉️ Richiesta inviata"
			keyboard=[[]]
			if (update['message']['from_user']['username']):
				username= update['message']['from_user']['username']
			else:
				username=""
			if(len(update.message.text.split(" "))==4) and ("@" in update.message.text.split(" ")[3]) and ("." in update.message.text.split( )[3]):
				textSend=str(update.message.text)+" "+username
				keyboard.append([InlineKeyboardButton("Accetta", callback_data=str(chat_id))])
				reply_markup2=InlineKeyboardMarkup(keyboard)
				bot.sendMessage(chat_id=-1001095167198,text=textSend,reply_markup=reply_markup2)
				bot.sendMessage(chat_id=chat_id, text=messageText)

			else:
				messageText="Errore compilazione /request:\n Forma esatta: /request <nome> <cognome> <e-mail> (il nome e il cognome devono essere scritti uniti Es: Di mauro -> Dimauro)"
				bot.sendMessage(chat_id=update.message.chat_id, text=messageText)


		else:
			messageText="Hai già effettuato la richiesta di accesso"
			bot.sendMessage(chat_id=update.message.chat_id, text=messageText)



	else:
		messageText="Non è possibile utilizzare /request in un gruppo"
		bot.sendMessage(chat_id=chat_id, text=messageText)

def adddb(bot, update):
	chat_id = update.message.chat_id
	if (chat_id==26349488 or chat_id==-1001095167198 or chat_id==46806104):
		ArrayValue=update.message.text.split(" ") #/add nome cognome e-mail username chatid
		if len(ArrayValue)==6:
			conn.execute("INSERT INTO 'Chat_id_List' VALUES ("+ArrayValue[5]+",'"+ArrayValue[4]+"','"+ArrayValue[1]+"','"+ArrayValue[2]+"','"+ArrayValue[3]+"') ")
			bot.sendMessage(chat_id=ArrayValue[5],text= "🔓 La tua richiesta è stata accettata")
			conn.commit()
		elif len(ArrayValue)==5:
			conn.execute("INSERT INTO 'Chat_id_List'('Chat_id','Nome','Cognome','Email') VALUES ("+ArrayValue[4]+",'"+ArrayValue[1]+"','"+ArrayValue[2]+"','"+ArrayValue[3]+"')")
			bot.sendMessage(chat_id=int(ArrayValue[4]),text= "🔓 La tua richiesta è stata accettata")
			conn.commit()
		else:
			bot.sendMessage(chat_id=chat_id,text="/adddb <nome> <cognome> <e-mail> <username> <chat_id>")

def drive(bot, update):
    checkLog(bot, update, "drive")

    settings_file = "config/settings.yaml"
    gauth = GoogleAuth(settings_file=settings_file)
    gauth.CommandLineAuth()
    #gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    chat_id=update.message.chat_id
    TestDB=0
    IDDrive='0B7-Gi4nb88hremEzWnh3QmN3ZlU'
    if chat_id < 0:
    	bot.sendMessage(chat_id=chat_id,text="La funzione /drive non è ammessa nei gruppi")
    else:
    	for row in conn.execute("SELECT Chat_id FROM 'Chat_id_List' "):
    		if row[0] == chat_id:
    			TestDB=1;

    	if TestDB==1:
            keyboard2=[[]];
            try:
                file_list = drive.ListFile({'q': "'"+IDDrive+"' in parents and trashed=false",'orderBy':'folder,title'}).GetList()
            except Exception as error:
                print str(error)
            NumberRow=0
            NumberArray=0

            for file1 in file_list:
                fileN=""
                if file1['mimeType']=="application/vnd.google-apps.folder":
                    if NumberRow>=3:
                        keyboard2.append([InlineKeyboardButton("🗂 "+file1['title'], callback_data=file1['id'])])
                        NumberRow=0
                        NumberArray+=1
                    else:
                        keyboard2[NumberArray].append(InlineKeyboardButton("🗂 "+file1['title'],callback_data=file1['id']))
                        NumberRow+=1
                else:
                    if NumberRow>=3:
                        keyboard2.append([InlineKeyboardButton("📃 "+file1['title'], callback_data=file1['id'])])
                        NumberRow=0
                        NumberArray+=1
                    else:
                        keyboard2[NumberArray].append(InlineKeyboardButton("📃 "+file1['title'],callback_data=file1['id']))
                        NumberRow+=1

            reply_markup3 = InlineKeyboardMarkup(keyboard2)
            bot.sendMessage(chat_id=chat_id,text="DMI UNICT - Appunti & Risorse:", reply_markup=reply_markup3)
    	else:
    		bot.sendMessage(chat_id=chat_id,text="🔒 Non hai i permessi per utilizzare la funzione /drive,\n Utilizzare il comando /request <nome> <cognome> <e-mail> (il nome e il cognome devono essere scritti uniti Es: Di mauro -> Dimauro) ")

def help(bot, update):
    checkLog(bot, update,"help")
    messageText = help_cmd()
    bot.sendMessage(chat_id=update.message.chat_id,text=messageText)

def rappresentanti(bot, update):
	checkLog(bot, update,"rappresentanti")
	messageText = rapp_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def rappresentanti_dmi(bot, update):
	checkLog(bot, update,"rappresentanti_dmi")
	messageText = rapp_dmi_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def rappresentanti_info(bot, update):
	checkLog(bot, update,"rappresentanti_info")
	messageText = rapp_inf_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def rappresentanti_mate(bot, update):
	checkLog(bot, update,"rappresentanti_mate")
	messageText = rapp_mat_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def prof(bot, update):
	checkLog(bot, update,"prof")
	messageText = prof_cmd(update.message.text)
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def mesami(bot, update):
	checkLog(bot, update,"mesami")
	messageText = 'http://web.dmi.unict.it/Didattica/Laurea%20Magistrale%20in%20Informatica%20LM-18/Calendario%20degli%20Esami'
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def aulario(bot, update):
	checkLog(bot, update,"aulario")
	messageText = 'http://aule.dmi.unict.it/aulario/roschedule.php'
	bot.sendMessage(chat_id=update.message.chat_id, text=messageText)

def smonta_portoni(bot, update):
	checkLog(bot, update,"smonta_portoni")
	messageText = smonta_portoni_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

def santino(bot, update):
	checkLog(bot, update,"santino")
	messageText = santino_cmd()
	bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

def liste(bot, update):
	checkLog(bot, update,"liste")
	picture = open("data/img/liste.png", "rb")
	messageText = "Liste e candidati"
	bot.sendPhoto(chat_id=update.message.chat_id, photo=picture)
	bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

def forum_bot(bot, update):
	checkLog(bot, update,"forum_bot")
	messageText = forum_cmd(update.message.text)
	bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

def news_(bot, update):
	if (update.message.chat_id == 26349488):
		global news
		news = update.message.text.replace("/news ", "")
		messageText = "News Aggiornata!"
		bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

def spamnews(bot, update):
	if(update.message.chat_id==26349488):
		chat_ids = open('logs/chatid.txt', 'r').read()
		chat_ids = chat_ids.split("\n")
		for i in range((len(chat_ids)-1)):
			try:
				if not "+" in chat_ids[i]:
					bot.sendMessage(chat_id=chat_ids[i], text=news)
			except Exception as error:
				open("logs/errors.txt", "a+").write(str(error)+" "+str(chat_ids[i])+"\n")
		messageText = "News spammata!"
		bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

def disablenews(bot, update):
	checkLog(bot, update,"disablenews")
	chat_ids = open('logs/chatid.txt', 'r').read()
	chat_id = update.message.chat_id
	if not ("+"+str(chat_id)) in chat_ids:
		chat_ids = chat_ids.replace(str(chat_id), "+"+str(chat_id))
		messageText= "News disabilitate!"
		open('logs/chatid.txt', 'w').write(chat_ids)
	else:
		messageText = "News già disabilitate!"
	bot.sendMessage(chat_id=update.message.chat_id, text= messageText)


def enablenews(bot, update):
	checkLog(bot, update,"enablenews")
	chat_ids = open('logs/chatid.txt', 'r').read()
	chat_id = update.message.chat_id
	if ("+"+str(chat_id)) in chat_ids:
		chat_ids = chat_ids.replace("+"+str(chat_id), str(chat_id))
		messageText = "News abilitate!"
		open('logs/chatid.txt', 'w').write(chat_ids)
	else:
		messageText = "News già abilitate!"
	bot.sendMessage(chat_id=update.message.chat_id, text= messageText)

# check if user (chatid) is registered on chatid.txt

def stats(bot,update):
    chat_id = update.message.chat_id
    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)
    if(len(update['message']['text'].split(' '))==2):
        days=int(update['message']['text'].split(' ')[1])
        if(days<=0):
            days=30
    else:
        days=30
    text=""
    dateCheck=unicode(date.today()-timedelta(days=days))
    text+="Record di "+str(days)+" giorni:\n"
    for row in conn.execute("SELECT Type, count(chat_id) FROM stat_list WHERE DateCommand > '"+dateCheck+"' GROUP BY Type ORDER BY Type;" ):
        text+=str(row[1])+": "+str(row[0])+"\n"
    bot.sendMessage(chat_id=chat_id,text=text)

def statsTot(bot,update):
    chat_id = update.message.chat_id
    conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)
    text=""
    text+="Record Globale:\n"
    for row in conn.execute("SELECT Type, count(chat_id) FROM stat_list GROUP BY Type ORDER BY Type;" ):
        text+=str(row[1])+": "+str(row[0])+"\n"
    bot.sendMessage(chat_id=chat_id,text=text)


def checkLog(bot, update,type):
    if (disable_db == 0):
        chat_id = update.message.chat_id
        conn = sqlite3.connect('data/DMI_DB.db',check_same_thread=False)
        today=unicode(date.today());
        conn.execute("INSERT INTO stat_list VALUES ('"+str(type)+"',"+str(chat_id)+",'"+str(today)+" ')");
        conn.commit()

    if (disable_chatid_logs == 0):
        log = open("logs/chatid.txt", "a+")
        if not str(chat_id) in log.read():
            log.write(str(chat_id)+"\n")
