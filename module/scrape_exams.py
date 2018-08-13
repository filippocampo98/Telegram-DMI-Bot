# -*- coding: utf-8 -*-

import bs4
import requests
import json
from time import localtime, strftime

def insert(row, session, items, year):
	item = {"insegnamento" : "", "docenti" : "", "prima" : ["", "", ""], "seconda" : ["", ""], "terza" : ["", ""], "straordinaria" : ["", ""], "anno" : year}
	item["insegnamento"] = (row[1]).text
	item["docenti"] = (row[2]).text
	for i in range(len(row))[3:]:
		if (row[i]).has_attr("class"):
			ses_temp = "straordinaria"
			(item[ses_temp])[i-3-2] = ((row[i]).text)
		elif (row[i]).text.strip() != "":
			(item[session])[i-3] = ((row[i]).text)
	items.append(item)

def handle_exams(row, session, items, year):
	flag = False
	for element in items:
		if row[1].text == element["insegnamento"]:
			flag = True
			for i in range(len(row))[3:]:
				if i <= len(element[session])-1:
					element[session][i-3] = row[i].text
	if not flag:
		insert(row, session, items, year)

def scrape_exams():
	url_exams = [
		"http://web.dmi.unict.it/corsi/l-31/esami?sessione=1&aa=118",
		"http://web.dmi.unict.it/corsi/l-31/esami?sessione=2&aa=118",
		"http://web.dmi.unict.it/corsi/l-31/esami?sessione=3&aa=118"
	]
	status = {
		"length": "" ,
		"lastupdate": strftime("%Y-%d-%m %H:%M:%S",localtime())
	}

	arr = ["prima", "seconda", "terza"]
	items = []
	year = ""

	for count, url in enumerate(url_exams):
		source = requests.get(url).text
		soup = bs4.BeautifulSoup(source, "html.parser")
		table = soup.find(id="tbl_small_font")
		all_tr = table.find_all("tr")

		for tr in all_tr:
			firstd = tr.find("td")
			if not tr.has_attr("class") and not firstd.has_attr("class"):
				all_td = tr.find_all("td")

				if count == 0:
					insert(all_td, arr[count], items, year)
				else:
					handle_exams(all_td, arr[count], items, year)
			elif not tr.has_attr("class") and firstd.has_attr("class"):
				year = firstd.b.text

	status["length"] = len(items)
	finaljson = {
		"status" : status,
		"items" : items
	}

	with open('data/json/esami.json', 'w') as outfile:
		json.dump(finaljson, outfile, sort_keys=True, indent=4)
