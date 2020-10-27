import os
import csv
import re
import io
import tokenize as T
from operator import itemgetter
import pymystem3 as Stem
import pymorphy2 as pm
import pymorphy2_dicts_ru
#from csv_rw_laba2 import csv_dict_reader


def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter='#')
    data = ["id#url#date#header#content"]
    data_splitted = []
    for line in reader:
        string = "{}#{}#{}#{}#{}".format(line["id"], line["url"], line["category"], line["name"], line["description"])
        data.append(string)
        data_splitted.append(str.split(string, "#"))
    return data_splitted


def checkExecTimeMystemOneText(texts):
    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    txtpart = lol(texts, 1000)
    res = []
    for txtp in txtpart:
        alltexts = ' '.join([txt + ' br ' for txt in txtp])
        m = Stem.Mystem()
        words = m.lemmatize(alltexts)
        doc = []
        for txt in words:
            if txt != '\n' and txt.strip() != '':
                if txt == 'br':
                    res.append(doc)
                    doc = []
                else:
                    doc.append(" "+txt+" ")
        return res


def del_of_spec_symbols(content):
    num_of_doc = 0
    for i in content:
        s = str(i)
        s = re.sub('[^A-Za-zА-Яа-я ё]+', ' ', s)
        s = re.sub(r'\s+', ' ', s)
        s = str.lower(s)
        content[num_of_doc] = s
        num_of_doc = num_of_doc + 1
    return content


def preprocessing(path):
    data = []
    with open(path, encoding='utf-8') as f_obj:
        data = csv_dict_reader(f_obj)
    content = [i[4] for i in data]
    content = del_of_spec_symbols(content)
    tokens = checkExecTimeMystemOneText(content)
    table = ["ID#Token#No. of document#Count#POS"]
    table_without_numeration = ["Token#No. of document#Count#POS"]
    num_of_doc = 0
    id = 0
    bag_of_words = "".join(["".join(doc) for doc in tokens])
    ma = pm.MorphAnalyzer()
    for doc in tokens:
        num_of_doc = num_of_doc + 1
        text_of_doc = "".join(doc)
        #print(text_of_doc)
        for g in doc:
            id = id + 1
            token = g
            #count = bag_of_words.count(token)
            count = text_of_doc.count(g)
            pos = str(ma.tag(token[1:-1])[0])[0:4]
            if table_without_numeration.count("{}#{}#{}#{}".format(token, num_of_doc, count, pos)) == 0:
                table.append("{}#{}#{}#{}#{}".format(id, token, num_of_doc, count, pos))
                table_without_numeration.append("{}#{}#{}#{}".format(token, num_of_doc, count, pos))
    del(table_without_numeration)
    return table


path = 'C:\Program Files\PycharmProjects\\new\\venv\ITvPS\laba1\\dict_output.csv'

if __name__ == "__main__":
    table = preprocessing(path)
    print(table)

