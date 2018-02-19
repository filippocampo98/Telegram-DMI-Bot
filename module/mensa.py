# encoding=utf8
import requests
import bs4
from os.path import exists, join

def scrap():

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
