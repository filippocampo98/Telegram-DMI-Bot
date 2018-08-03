# -*- coding: utf-8 -*-

import bs4
import requests
import json


def getanagrafica(linkscheda):
    diz = {"ufficio": "", "email": "", "sito": "", "telefono": "", "fax": ""}
    sorgente = requests.get("http://web.dmi.unict.it"+str(linkscheda)).text
    soup = bs4.BeautifulSoup(sorgente, "html.parser")
    div = soup.find(id="anagrafica")
    for bi in div.find_all("b"):
        if bi.text == "Ufficio:":
            diz['ufficio'] = bi.next_sibling
        elif bi.text == "Email:":
            diz['email'] = bi.next_sibling.next_sibling.text
        elif bi.text == "Sito web:":
            diz['sito'] = bi.next_sibling.next_sibling.text
        elif bi.text == "Telefono:":
            diz['telefono'] = bi.next_sibling
        elif bi.text == "Fax:":
            diz['fax'] = bi.next_sibling
    return diz


def scrape_prof():
    url_prof = "http://web.dmi.unict.it/docenti"
    items = []
    count = 0
    contratto = False
    madrelingua = False
    href = ""
    cognome = ""
    nome = ""
    ruolo = ""
    sorgente = requests.get(url_prof).text
    soup = bs4.BeautifulSoup(sorgente, "html.parser")
    table = soup.find(id="persone")
    for link in table.find_all("a"):
        if not link.has_attr("name"):
            href = link['href']
            cognome = link.text.split(" ")[0]
            nome = ""
            for i in range(len(link.text.split(" "))-1):
                nome += link.text.split(" ")[i+1] + " "
            if contratto:
                ruolo = "Contratto"
            elif madrelingua:
                ruolo = "Lettore madrelingua"
            else:
                ruolo = link.parent.next_sibling.text.split(" ")[1] if len(
                    link.parent.next_sibling.text.split(" ")) > 1 else link.parent.next_sibling.text
            if link.parent.parent.next_sibling.next_sibling != None and link.parent.parent.next_sibling.next_sibling.find("td").find("b") != None:
                if not contratto:
                    contratto = True
                else:
                    contratto = False
                    madrelingua = True
            count += 1
            anagrafica = getanagrafica(href)
            items.append({"ID": count, "Ruolo": ruolo.title(), "Nome": nome,
                          "Cognome": cognome, "Scheda DMI": "http://web.dmi.unict.it" + href,
                          "Fax": anagrafica['fax'], "Telefono": anagrafica['telefono'],
                          "Email": anagrafica['email'], "Ufficio" : anagrafica['ufficio'],
                          "Sito" : anagrafica['sito']})
    with open('data/json/professori.json', 'w') as outfile:
        json.dump(items, outfile, sort_keys=True, indent=4)
