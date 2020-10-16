# -*- coding: utf-8 -*-

import json
import sqlite3

def get_nome_giorno(day):
    switcher = {
        '1' : 'Lunedì',
        '2' : 'Martedì',
        '3' : 'Mercoledì',
        '4' : 'Giovedì',
        '5' : 'Venerdì'
    }

    return switcher.get(day, "Giorno non valido")

def lezioni_cmd(userDict):
    output_str = []

    where_giorno = " or giorno_settimana = ".join([key.replace("giorno", "") for key in userDict if "giorno" in key])  # stringa contenente le sessioni per cui il dict contiene la key, separate da " = '[]' and not "
    where_anno = " or anno = ".join([key.replace(" anno", "") for key in userDict if "anno" in key]) # stringa contenente gli anni per cui il dict contiene la key, separate da "' or anno = '"
    where_insegnamento = userDict.get("insegnamento", "") # stringa contenente l'insegnamento, se presente

    if where_giorno:
        where_giorno = f"and (giorno_settimana = {where_giorno})"
    else:
        where_giorno = ""
    if where_anno:
        where_anno = f"and (anno = {where_anno})"
    else:
        where_anno = ""

    query = f"""SELECT nome, giorno_settimana, ora_inizio, ora_fine, aula, anno 
				FROM lessons
				WHERE nome LIKE ? {where_giorno} {where_anno}"""

    conn = sqlite3.connect("data/DMI_DB.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    try:
        cur.execute(query, ('%' + where_insegnamento + '%',))
    except Exception as e:
        print("The following lessons query could not be executed (command \\lezioni)")
        print(query)  # per controllare cosa è andato storto
        print("[error]: " + str(e))

    for item in cur.fetchall():
        output_str.append(lezioni_output(item))

    return check_output(output_str)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def lezioni_output(item):
    output = "*Insegnamento:* " + item["nome"]
    output += "\n*Giorno:* " + get_nome_giorno(item["giorno_settimana"])
    output += "\n*Ora:* " + item["ora_inizio"] + "-" + item["ora_fine"]
    output += "\n*Anno:* " + str(item["anno"])
    output += "\n*Aula:* " + str(item["aula"]) + "\n"
    return output


def check_output(output):
    if len(output):
        output_str = "\n".join(output)
        output_str += "\nRisultati trovati: " + str(len(output))
    else:
        output_str = "Nessun risultato trovato :(\n"

    return output_str
