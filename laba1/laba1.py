import csv
import requests
import re
import time
from bs4 import BeautifulSoup

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", encoding='utf8', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter='#', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# var 1
def requester_with_soup_first(base_url, amount, delay_time):
    r = requests.get(BASE_URL)
    soap = BeautifulSoup(r.text, features="html.parser")
    ases = soap.find_all("a")
    data = ["id#url#date#header#content"]
    regexp = re.compile('[\/][n][e][w][s][\/].*')
    id = 0
    for i in ases:
        href = i.get("href")
        if regexp.match(str(href)) != None:
            id = id + 1
            url = "https://lenta.ru" + href
            if delay_time != 0:
                time.sleep(delay_time)
            r_page = requests.get(url)
            page = BeautifulSoup(r_page.text, features="html.parser")
            page_content = BeautifulSoup(str(page.find("div", {"class": "b-topic__content"})), features="html.parser")
            ppp = str(page_content.find_all("p"))
            content = BeautifulSoup(ppp, features="html.parser").text[1:-1].replace(".,", ".")
            date = page_content.time.contents[0]
            header = str(page_content.h1.contents[0]).replace("\\xa0", " ")
            data.append("{}#{}#{}#{}#{}".format(id, url, date, header, content))
            print(id)
            if id == amount: break
    return data

#var 2
def requester_with_soup_second_var(base_url, amount, delay_time):
    r = requests.get(BASE_URL)
    soap = BeautifulSoup(r.text, features="html.parser")
    div1 = str(soap.find("div", {"class": "touchcarousel-container"}))
    soap_div1 = BeautifulSoup(str(div1), features="html.parser")
    div2 = soap_div1.find_all("div", {'class':'touchcarousel-item ctg-slider__wrap top_goods'})
    #print(div2)
    data = ["id#url#category#name#description"]
    id = 0
    for i in div2:
        id = id + 1
        print(id)
        url = "https://www.e-katalog.ru" + i.a.get("href")
        if delay_time != 0:
            time.sleep(delay_time)
        r_page = requests.get(url)
        page = BeautifulSoup(r_page.text, features="html.parser")
        header = str.split(page.h1.text)
        categ = header[0]
        name = " ".join(header[1:])
        desc = page.find("div", {'class':'conf-desc-ai-title'}).text
        data.append("{}#{}#{}#{}#{}".format(id, url, categ, name, desc))
        if id == amount: break
    return data

#var 1
#BASE_URL = 'https://lenta.ru/rubrics/economics/'
BASE_URL = 'https://www.e-katalog.ru/k265.htm'
data = requester_with_soup_second_var(BASE_URL, 70, 0)

if __name__ == "__main__":
    data = [i.replace("\\xa0", " ").split("#") for i in data]
    print("OK")
    my_list = []
    print(data)
    fieldnames = data[0]
    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)
    path = "dict_output.csv"
    csv_dict_writer(path, fieldnames, my_list)
