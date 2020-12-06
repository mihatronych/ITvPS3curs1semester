import pymystem3 as Stem
import os
import re
import math
import csv
from nltk.corpus import stopwords

_stopwords = set(stopwords.words('russian') + list('``'))

def get_tf_idf(my_docs, my_dict):
    tf_idf = {}
    my_dict = list(my_dict)
    tf2 = [[0.0] * len(my_dict) for i in range(len(my_docs))]
    for i in range(len(my_docs)):
        for j in range(len(my_dict)):
            if my_dict[j] in my_docs[i]:
                tf2[i][j] = my_docs[i].count(my_dict[j]) / len(my_docs[i])
    for i in range(len(my_dict)):
        c = []
        for j in range(len(my_docs)):
            if my_dict[i] in my_docs[j]:
                c.append(math.fabs(tf2[j][i] * math.log2(len(my_docs[j]) / sum([1.0 for z in my_docs if my_dict[i] in z]))))
            else:
                c.append(0)
        tf_idf[my_dict[i]] = c
    return tf_idf


def centr_coords(tf_idf_table, docs_of_class, tfidf_columns_start):
    Dc = len(docs_of_class)
    mu = []
    word_mu = {}
    for i in tf_idf_table.keys():
        vs = sum(tf_idf_table[i][tfidf_columns_start: len(docs_of_class)])/Dc
        mu.append(vs)
        word_mu[i] = vs
    return word_mu

def roccio_classificate(text, words_tf_idf, mu_classes, text_num):
    dif_eucl1 = 0.0
    dif_eucl2 = 0.0
    for c in range(2):
        for w in text:
            if w in words_tf_idf.keys():
                if c == 0:
                    D = float(words_tf_idf[w][text_num])
                    dif_eucl1 += (float(mu_classes[w][c]) - D) * (float(mu_classes[w][c]) - D)
                else:
                    D = float(words_tf_idf[w][text_num])
                    dif_eucl2 += (float(mu_classes[w][c]) - D) * (float(mu_classes[w][c]) - D)
    dif_eucl1 = math.sqrt(dif_eucl1)
    dif_eucl2 = math.sqrt(dif_eucl2)
    if dif_eucl1 < dif_eucl2:
        return (dif_eucl1, dif_eucl2, "Рубрика спорт", "Рубрика технологии")
    else:
        return (dif_eucl1, dif_eucl2, "Рубрика технологии", "Рубрика спорт")


def txt_reader(path):
    tutu = {}
    for file in os.listdir(path):
        if file.endswith(".txt"):
            if file.endswith("all.txt") != True:
                pathh = os.path.join(path, file)
                with open(pathh, encoding='utf-8') as f_obj:
                    tutu[file] = f_obj.read()
    return tutu

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
            if txt != '\n' and txt.strip() != '' and _stopwords.__contains__(txt) != True:
                if txt == 'br':
                    res.append(doc)
                    doc = []
                else:
                    doc.append(" "+txt+" ")
        return res


def bag_of_tokenized(tokens):
    bag_of_words = set()
    for i in tokens:
        some_set = set(i)
        bag_of_words.update(some_set)
    return bag_of_words


def del_of_spec_symbols(content):
    s = str(content)
    s = re.sub('[^A-Za-zА-Яа-я ё]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    s = str.lower(s)
    return s

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def uber_table_write_in_csv(uber_table):
    data = ["term, 1, 2, 3, 4, 5 ,6 ,7 ,8 ,9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 ,26 ,27 ,28 ,29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40".split(",")]
    for el in uber_table.items():
        data.append([el[0]] + el[1])
    my_list = []
    fieldnames = data[0]
    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)

    path = "tf_idf.csv"
    csv_dict_writer(path, fieldnames, my_list)

def mu_table_write_in_csv(uber_table):
    data = ["term, C1, C2".split(",")]
    for el in uber_table.items():
        data.append([el[0]] + el[1])
    my_list = []
    fieldnames = data[0]
    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)

    path = "trained.csv"
    csv_dict_writer(path, fieldnames, my_list)

def csv_dict_reader_tfidf(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    data = ["term; 1; 2; 3; 4; 5; 6; 7; 8; 9; 10; 11; 12; 13; 14; 15; 16; 17; 18; 19; 20; 21; 22; 23; 24; 25 ;26 ;27 ;28 ;29; 30; 31; 32; 33; 34; 35; 36; 37; 38; 39; 40"]
    data_splitted = []
    vect_table = {}
    for line in reader:
        f = line.keys()
        string = "{}; {}; {}; {}; {}; {}; {}; {}; {}; {};{}; {}; {}; {}; {}; {}; {}; {}; {}; {};{}; {}; {}; {}; {}; {}; {}; {}; {}; {};{}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}".format(
            line["term"], line[" 1"], line[" 2"], line[" 3"], line[" 4"], line[" 5 "], line["6 "], line["7 "], line["8 "], line["9"], line[" 10"],
            line[" 11"], line[" 12"], line[" 13"], line[" 14"], line[" 15"], line[" 16"], line[" 17"], line[" 18"], line[" 19"], line[" 20"],
        line[" 21"], line[" 22"], line[" 23"], line[" 24"], line[" 25 "], line["26 "], line["27 "], line["28 "], line["29"], line[" 30"],
        line[" 31"], line[" 32"], line[" 33"], line[" 34"], line[" 35"], line[" 36"], line[" 37"], line[" 38"], line[" 39"], line[" 40"])
        data.append(string)
        data_splitted.append(str.split(string, ";"))
        vect_table[str.split(string, ";")[0]] = str.split(string, ";")[1:]
    return vect_table

def csv_dict_reader_mu(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    data = ["title;keywords;annotation;class"]
    data_splitted = []
    vect_table = {}
    for line in reader:
        f = line.keys()
        string = "{};{};{}".format(line["term"], line[" C1"], line[" C2"])
        data.append(string)
        data_splitted.append(str.split(string, ";"))
        vect_table[str.split(string, ";")[0]] = str.split(string, ";")[1:]
    return vect_table

if __name__ == "__main__":
    path = "news_yandex/"
    txts = txt_reader(path)
    txt_preprocessed = [del_of_spec_symbols(i) for i in txts.values()]

    #doc_txts = checkExecTimeMystemOneText(list(txts.values())[17:19] + list(txts.values())[37:40])
    #doc_txts = checkExecTimeMystemOneText(txt_preprocessed)
    #print(doc_txts)
    #my_dict = bag_of_tokenized(doc_txts)
    #tf_idf = get_tf_idf(doc_txts, my_dict)
    #uber_table_write_in_csv(tf_idf)
    #c1 = centr_coords(tf_idf,doc_txts[:16],1)
    #c2 = centr_coords(tf_idf,doc_txts[:36],21)
    #mu_table = {}
    #for w in c1.keys():
    #    mu_table[w] = [c1[w], c2[w]]
    #mu_table_write_in_csv(mu_table)
    doc_txts = checkExecTimeMystemOneText(txt_preprocessed[17:20] + txt_preprocessed[37:40])
    with open("tf_idf.csv", "r", encoding='utf-8') as f_obj:
        tf_idf = csv_dict_reader_tfidf(f_obj)
    with open("trained.csv", "r", encoding='utf-8') as f_obj:
        roccio = csv_dict_reader_mu(f_obj)
    print(doc_txts[0])
    class_res = roccio_classificate(doc_txts[0], tf_idf, roccio, 17)
    print(class_res)
    print(doc_txts[1])
    class_res = roccio_classificate(doc_txts[1], tf_idf, roccio, 18)
    print(class_res)
    print(doc_txts[2])
    class_res = roccio_classificate(doc_txts[2], tf_idf, roccio, 19)
    print(class_res)
    print(doc_txts[3])
    class_res = roccio_classificate(doc_txts[3], tf_idf, roccio, 37)
    print(class_res)
    print(doc_txts[4])
    class_res = roccio_classificate(doc_txts[4], tf_idf, roccio, 38)
    print(class_res)
    print(doc_txts[5])
    class_res = roccio_classificate(doc_txts[5], tf_idf, roccio, 39)
    print(class_res)