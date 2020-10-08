# -*- coding: utf-8 -*-

import json
import requests
import sqlite3
import calendar
import datetime
import locale
import time
from module.scraper_lessons import get_giorno

locale.setlocale(locale.LC_ALL, 'it_IT.utf8')

def get_numero_giorno(giorno):
    switcher = {
        'lunedi':'1',
        'martedi':'2',
        'mercoledi':'3',
        'giovedi':'4',
        'venerdi':'5'
    }

    return switcher.get(giorno, "Giorno non valido")

def get_numero_anno(anno):
    switcher = {
        'primo':1,
        'secondo':2,
        'terzo':3
    }

    return switcher.get(anno, "Anno non valido, utilizzare primo/secondo/terzo")

def lezioni_output(item):
    daylist = list(calendar.day_name)

    output = "*Nome:* " + item["nome"]
    output += "\n*Aula:* " + str(item["aula"])

    for day in daylist:
        numero_giorno = get_numero_giorno(day.replace('ì','i'))
        if(numero_giorno == item['giorno_settimana']):
            output += "\n*Giorno:* " + day.title()

    output += "\n*Anno:* " + str(item["anno"]) + "\n"

    return output

def lezioni_condition(items, condition, *arg):
    output = set()
    for item in items:
        if(arg):
            if( (arg[0] in str(item[condition]).lower()) or (get_numero_anno(arg[0]) == item[condition]) ):
                output.add(lezioni_output(item))
        else:
            if(get_numero_giorno(condition) in item['giorno_settimana']):
                output.add(lezioni_output(item))

    return output

def lezioni_condition_mult(items, days, years):
    output = set()
    for item in items:
        for day in days:
            for year in years:
                if (get_numero_anno(year) == item['anno'] and get_numero_giorno(day) == item['giorno_settimana']):
                    output.add(lezioni_output(item))
    return output

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def lezioni_cmd(bot, update, args):

    output_str = "Poffarbacco, qualcosa non va. Segnalalo ai dev /contributors \n"

    if args:
        output = set()

        conn = sqlite3.connect('data/DMI_DB.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("SELECT * FROM lessons")
        items = cur.fetchall()
        conn.close()

        daylist = list(calendar.day_name)
        daylist = [str(x).lower().replace('ì', 'i') for x in daylist]
        #Clear arguments - Trasform all to lower case utf-8 (ì) - Remove word 'anno' and len<2
        args = [str(x).lower().replace('ì', 'i') for x in args if len(x) > 2]

        try:

            if 'anno' in args: args.remove('anno')

            #Study case
            if(len(args) == 1):
                
                if(args[0] in daylist):
                    output = lezioni_condition(items, args[0])

                elif(args[0] == "oggi"):
                    output = lezioni_condition(items, time.strftime("%A").replace('ì', 'i'))

                elif(args[0] == "domani"):
                    tomorrow_date = datetime.datetime.today() + datetime.timedelta(1)
                    tomorrow_name = datetime.datetime.strftime(tomorrow_date,'%A').replace('ì', 'i')
                    output = lezioni_condition(items, tomorrow_name)

                elif(args[0] in ("primo", "secondo", "terzo")):
                    output = lezioni_condition(items, "anno", args[0])

                elif([str(item["nome"]).lower().find(args[0]) for item in items]):
                    output = lezioni_condition(items, "nome", args[0])

                if not len(output):
                    output_str = "Nessun risultato trovato :(\n"
                else:
                    output_str = "\n".join(str(e) for e in output)

            elif(len(args) > 1):

                #Create an array of days and years if in arguments
                days = list(set(args).intersection(daylist))
                years = list(set(args).intersection(("primo", "secondo", "terzo")))

                if(days and years):
                    output = lezioni_condition_mult(items, days, years)

                elif("oggi" in args and years):
                    day = [time.strftime("%A").replace('ì', 'i')]
                    output = lezioni_condition_mult(items, day, years)

                elif("domani" in args and years):
                    tomorrow_date = datetime.datetime.today() + datetime.timedelta(1)
                    tomorrow_name = datetime.datetime.strftime(tomorrow_date,'%A').replace('ì','i')
                    day = [tomorrow_name]
                    output = lezioni_condition_mult(items, day, years)

                else:
                    for arg in args:
                        output = output.union(lezioni_condition(items, "nome", arg))

                if not len(output):
                    output_str = "Nessun risultato trovato :(\n"
                else:
                    output_str = "\n\n".join(str(e) for e in output)

        except Exception as e:
            #debugging
            bot.sendMessage(chat_id=update.message.chat_id, text=str(e))

    else:
        output_str = "Inserisci almeno uno dei seguenti parametri: giorno, materia, anno."

    return output_str
