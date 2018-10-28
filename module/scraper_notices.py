import requests
import bs4
import ast
import os

BASE_URL = "http://web.dmi.unict.it"
    
notices_urls = {
    "Informatica L-31": "http://web.dmi.unict.it/corsi/l-31/avvisi/",
    "Matematica L-35": "http://web.dmi.unict.it/corsi/l-35/avvisi/",
    "Informatica LM-18": "http://web.dmi.unict.it/corsi/lm-18/avvisi/",
    "Matematica LM-40": "http://web.dmi.unict.it/corsi/lm-40/avvisi/"
}

files = {
    'archive': 'data/archivioAvvisi.dat',
    'pending': 'data/avvisiInSospeso.dat',
    'notice': 'data/avviso.dat'
}

def get_links(label, url):
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.content, 'html.parser')

    result = soup.select("span.field-content a")

    return [
        {label: link.get('href')}
        for link in result
    ]

def get_content(url):
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.content, "html.parser")

    title = soup.find("h1", attrs={"class": "page-title"}).get_text()
    content = soup.find("div", attrs={"class": "field-item even"}).get_text()

    return title, content

def pull_pending_notice(file_name=files['pending']):
    if os.path.isfile(file_name):
        data = []

        with open(file_name, 'r') as fr:
            data = fr.read().splitlines(True)

        with open(file_name, 'w') as fw:
            fw.writelines(data[1:])

        if len(data) > 0:
            return ast.literal_eval(data[0])
    return None

def get_notice_content(notice_dict):
    label = list(notice_dict.keys())[0]
    url = "%s%s" % (BASE_URL, notice_dict[label])

    title, content = get_content(url)
    formatted_notice = '<b>[%s]</b>\n%s\n<b>%s</b>\n%s' % (label, url, title, content)

    with open(files['archive'], 'a') as fw:
        fw.write('%s\n' % notice_dict)

    with open(files['archive'], 'r') as fr:
        data = fr.read().splitlines(True)

        if len(data) > 50:
            with open(files['archive'], 'w') as fw:
                fw.writelines(data[1:])
    
    with open(files['notice'], 'w') as fw:
        fw.write(formatted_notice)

def scrape_notices():
    pending_notice = pull_pending_notice()

    if pending_notice:
        get_notice_content(pending_notice)
    else:
        notices = []

        for label, url in notices_urls.items():
            notices.extend(get_links(label, url))

        with open(files['pending'], 'a') as pending_file_handle:
            if os.path.isfile(files['archive']):
                with open(files['archive'], 'r') as archive_file_handle:
                    archive_notices = archive_file_handle.read()

                    for notice in notices:
                        if str(notice) not in archive_notices:
                            pending_file_handle.write("%s\n" % notice)
            else:
                for notice in notices:
                    pending_file_handle.write("%s\n" % notice)

        pending_notice = pull_pending_notice()
        if pending_notice:
            get_notice_content(pending_notice)
