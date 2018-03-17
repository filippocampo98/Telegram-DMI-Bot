# coding=utf-8

import bs4
import requests
import json
from time import localtime, strftime

def scrape_esami():
	url_esami = ["http://web.dmi.unict.it/corsi/l-31/esami?sessione=1&aa=118", "http://web.dmi.unict.it/corsi/l-31/esami?sessione=2&aa=118", "http://web.dmi.unict.it/corsi/l-31/esami?sessione=3&aa=118"]
	status = {"length": "" , "lastupdate": strftime("%Y-%d-%m %H:%M:%S", localtime())}
	arr = ["prima", "seconda", "terza"]
	items = []
	anno = ""
	for count, url in enumerate(url_esami):
		sorgente = requests.get(url).text
		soup = bs4.BeautifulSoup(sorgente, "html.parser")
		table = soup.find(id="tbl_small_font")
		all_tr = table.find_all("tr")
		for tr in all_tr:
			if not tr.has_attr("class"):
				firstd = tr.find("td")
				if not firstd.has_attr("class"):
					all_td = tr.find_all("td")
					sessione = arr[count]
					if count == 0:
						item = {"insegnamento" : "", "docenti" : "", "prima" : ["", "", ""], "seconda" : ["", "", ""], "terza" : ["", "", ""], "straordinaria" : ["", ""], "anno" : anno}
						item["insegnamento"] = (all_td[1]).text
						item["docenti"] = (all_td[2]).text
						for i in range(len(all_td))[3:]:
							if (all_td[i]).has_attr("class"):
								ses_temp = "straordinaria"
								(item[ses_temp])[i-3-2] = ((all_td[i]).text)
							elif (all_td[i]).text.strip() != "":
								(item[sessione])[i-3] = ((all_td[i]).text)
						items.append(item)
					else:
						for element in items:
							if (all_td[1]).text == element["insegnamento"]:
								for i in range(len(all_td))[3:]:
									(element[sessione])[i-3] = ((all_td[i]).text)
				else:
					anno = firstd.b.text
	status["length"] = len(items);
	finaljson = {"status" : status, "items" : items}
	with open('data/json/esami.json', 'w') as outfile:
		json.dump(finaljson, outfile, sort_keys=True, indent=4)

