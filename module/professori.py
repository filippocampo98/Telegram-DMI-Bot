# -*- coding: utf-8 -*-

import json

def prof_output(prof):
    output = "*Ruolo:* " + prof["Ruolo"] + "\n"
    output += "*Cognome:* " + prof["Cognome"] + "\n"
    output += "*Nome:* " + prof["Nome"] + "\n"
    if prof['Email'] != "":
        output += "*Indirizzo email:* " + prof["Email"] + "\n"
    if prof['Scheda DMI'] != "":
        output += "*Scheda DMI:* " + prof["Scheda DMI"] + "\n"
    if prof['Sito'] != "":
        output += "*Sito web:* " + prof["Sito"] + "\n"
    if prof['Ufficio'] != "":
        output += "*Ufficio:* " + prof["Ufficio"] + "\n"
    if prof['Telefono'] != "":
        output += "*Telefono:* " + prof["Telefono"] + "\n"
    if prof['Fax'] != "":
        output += "*Fax:* " + prof["Fax"] + "\n"
    return output

def prof_cmd(profs):

    if(profs):

        output = set()
        profs = [x.lower().encode('utf-8') for x in profs if len(x) > 3]

        with open("data/json/professori.json") as data_file:
            professori_data = json.load(data_file)
        for prof in profs:
            professori = [professore for professore in professori_data if (prof in professore["Nome"].lower() or prof in professore["Cognome"].lower())]
            for professore in professori:
                output.add(prof_output(professore))

        if(len(output)):
            output_str = '\n'.join(list(output))
        else:
            output_str = "Nessun risultato trovato :(\n"

    else:
        output_str = "La sintassi del comando è: /prof <nomeprofessore>\n"

    return output_str
