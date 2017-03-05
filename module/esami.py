# -*- coding: utf-8 -*-

from sets import Set

import json
import requests

def esami_output(item, sessions):

    output = "*Insegnamento:* " + item["insegnamento"]
    output += "\n*Docenti:* " + item["docenti"]

    for session in sessions:
        appeal = [appeal for appeal in item[session] if appeal]
        if(appeal):
            output += "\n*" + session.title() + ":* " + " | ".join(appeal)

    output += "\n*Anno:* " + item["anno"] + "\n"

    return output

def esami_condition(items, field, value, *session):
    output = Set()
    if(session):
        for item in items:
            if([appeal for appeal in item[value] if appeal]):
                output.add(esami_output(item, [value]))
    else:
        for item in items:
            if(value in item[field].lower()):
                output.add(esami_output(item, ("prima", "seconda", "terza", "straordinaria")))

    return output

def esami_cmd(args, link):

    output_str = "Poffarbacco, qualcosa non va. Segnalalo ai dev /contributors \n"

    if(args):
        output = Set()
        r = requests.get(link)
        if(r.status_code == requests.codes.ok):

            items = r.json()["items"]

            #Clear arguments - Trasform all to lower case - Remove word 'anno', 'sessione'
            args = [x.lower().encode('utf-8') for x in args if len(x) > 2]
            if 'anno' in args: args.remove('anno')
            if 'sessione' in args: args.remove('sessione')

            #Study case
            if(len(args) == 1):

                if(args[0] in ("primo", "secondo", "terzo")):
                    output = esami_condition(items, "anno", args[0])

                elif(args[0] in ("prima", "seconda", "terza", "straordinaria")):
                    output = esami_condition(items, "sessione", args[0], True)

                elif([item["insegnamento"].lower().find(args[0]) for item in items]):
                    output = esami_condition(items, "insegnamento", args[0])

                if(len(output)):
                    output_str = '\n'.join(list(output))
                    output_str += "\n_Risultati trovati: " + str(len(output)) + "/" + str(r.json()["status"]["length"]) + "_"
                    output_str += "\n_Ultimo aggiornamento: " + r.json()["status"]["lastupdate"] + "_\n"

                else:
                    output_str = "Nessun risultato trovato :(\n"

            elif(len(args) > 1):

                #Create an array of session and years if in arguments
                sessions = list(set(args).intersection(("prima", "seconda", "terza", "straordinaria")))
                years = list(set(args).intersection(("primo", "secondo", "terzo")))

                if(sessions and years):
                    for item in items:
                        if(item["anno"].lower().replace("anno","").replace(" ", "") in years):
                            if( [session for session in sessions if [appeal for appeal in item[session] if appeal]] ):
                                output.add(esami_output(item, sessions))

                elif(sessions and not years):
                    #If years array is empty and session not, the other word are subjects
                    subjects = [arg for arg in args if arg not in(sessions)]

                    for item in items:
                        if(subjects):
                            for subject in subjects:
                                if( [session for session in sessions if [appeal for appeal in item[session] if appeal]] ):
                                    if(subject in item["insegnamento"].lower()):
                                        output.add(esami_output(item, sessions))

                        #List of session of all years [useless]
                        '''
                        else:
                            if( [session for session in sessions if [appeal for appeal in item[session] if appeal]] ):
                                output.add(esami_output(item, sessions))
                        '''

                elif(not sessions and not years):
                    for arg in args:
                        output = output.union(esami_condition(items, "insegnamento", arg))

                if(len(output)):
                    output_str = '\n'.join(list(output))
                    output_str += "\n_Risultati trovati: " + str(len(output)) + "/" + str(r.json()["status"]["length"]) + "_"
                    output_str += "\n_Ultimo aggiornamento: " + r.json()["status"]["lastupdate"] + "_\n"
                else:
                    output_str = "Nessun risultato trovato :(\n"
    else:
        output_str = "Inserisci almeno uno dei seguenti parametri: giorno, materia, sessione (prima, seconda, terza, straordinaria)."

    return output_str
