# -*- coding: utf-8 -*-

from sets import Set
import json

def prof_output(prof):
    output = "*Ruolo:* " + prof["Ruolo"] + "\n"
    output += "*Cognome:* " + prof["Cognome"] + "\n"
    output += "*Nome:* " + prof["Nome"] + "\n"
    output += "*Indirizzo email:* " + prof["Email"] + "\n"
    output += "*Sito web:* " + prof["Sito"] + "\n"
    output += "*Scheda DMI:* " + prof["SchedaDMI"] + "\n"
    return output

def prof_cmd(profs):

    output_str = "Poffarbacco, qualcosa non va. Segnalalo ai dev \contributors \n"

    if(profs):

        output = Set()
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
