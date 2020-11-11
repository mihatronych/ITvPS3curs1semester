import csv
import re
import pymystem3 as Stem
import pymorphy2 as pm
from ITvPS.laba4.preprocessing_laba_2 import csv_dict_reader
from ITvPS.laba4.vectoriser_laba_3 import get_bag_of_stemmed_words, text_stemmer, txt_reader, txt_parser, txt_tokenizer, \
    bool_tf_tfidf, bag_of_tokenized
from nltk.stem.snowball import RussianStemmer
from ITvPS.laba2.csv_rw_laba2 import csv_dict_writer
import math

def csv_safe(vect):
    data = [i for i in vect.items()]
    my_list = []
    headers = []
    c = 0
    for vec in vect.values():
        c = len(vec)
        break
    for i in range(c):
        if i == 0:
            headers.append("Term")
        else:
            headers.append("Текст_" + str(i))
    fieldnames = headers
    for values in data:
        val = [values[0]]
        val.extend(values[1])
        inner_dict = dict(zip(fieldnames, val))
        my_list.append(inner_dict)
    path = "db.csv"
    csv_dict_writer(path, fieldnames, my_list)

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", encoding='utf8', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter='#', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def index(pathh):
    cont = txt_reader(pathh)
    cont = txt_parser(cont)
    stem = RussianStemmer(False)
    stemmed_text = text_stemmer(cont, stem)
    token = stemmed_tokenizer(stemmed_text)
    token.append([])
    vect_tfidf = bool_tf_tfidf(token)[2]
    csv_safe(vect_tfidf)
    return vect_tfidf


def stemmed_tokenizer(texts):
    res = []
    doc = []
    alltexts = ' '.join([' '.join(tx) + ' br ' for tx in texts])
    for w in alltexts.split(" "):
        if w != '\n' and w.strip() != '':
            if w == 'br':
                res.append(doc)
                doc = []
            else:
                doc.append(" " + w + " ")
    return res


def formating_request(request):
    request = request + "Документ № 1*******************************************"
    return request


def sim_cosine(vect1, vect2):
    numerator = 0.0
    denominator_part_vect_1 = 0.0
    denominator_part_vect_2 = 0.0
    for i in range(len(vect1)):
        numerator += vect1[i] * vect2[i]
        denominator_part_vect_1 += vect1[i] * vect1[i]
        denominator_part_vect_2 += vect2[i] * vect2[i]
    sim = numerator / (denominator_part_vect_1 ** (1 / 2) * denominator_part_vect_2 ** (1 / 2))
    return sim

def get_tf_idf(my_docs, my_dict):
    tf_idf = {}
    my_dict = list(my_dict)
    tf2 = [[0.0] * len(my_dict) for i in range(len(my_docs))]
    for i in range(len(my_docs)):
        for j in range(len(my_dict)):
            if my_dict[j][1:-1] in my_docs[i]:
                tf2[i][j] = my_docs[i].count(my_dict[j][1:-1]) / len(my_docs[i])
    for i in range(len(my_dict)):
        c = []
        for j in range(len(my_docs)):
            if my_dict[i][1:-1] in my_docs[j]:
                c.append(math.fabs(tf2[j][i] * math.log2(len(my_docs[j]) / sum([1.0 for z in my_docs if my_dict[i][1:-1] in z]))))
            else:
                c.append(0)
        tf_idf[my_dict[i]] = c
    return tf_idf

def jaccard(vect1, vect2):
    numerator = 0.0
    denominator = 0.0
    for i in range(len(vect1)):
        numerator += min(vect1[i], vect2[i])
        denominator += max(vect1[i], vect2[i])
    jac = numerator / denominator
    return jac


def dice(vect1, vect2):
    numerator = 0.0
    denominator = 0.0
    for i in range(len(vect1)):
        numerator += min(vect1[i], vect2[i])
        denominator += vect1[i] + vect2[i]
    dice = 2 * numerator / denominator
    return dice


def sim_cosine_table(vects):
    req_vect = [i[0] for i in vects.values()]
    all_vects = [i for i in vects.values()]
    sim_ar = []
    for vect in vects.values():
        for i in range(len(vect)):
            cur_vect = [k[i] for k in all_vects]
            sim_ar.append(sim_cosine(req_vect, cur_vect))
        break
    return sim_ar


def jaccard_table(vects):
    req_vect = [i[0] for i in vects.values()]
    all_vects = [i for i in vects.values()]
    jac_ar = []
    for vect in vects.values():
        for i in range(len(vect)):
            cur_vect = [k[i] for k in all_vects]
            jac_ar.append(jaccard(req_vect, cur_vect))
        break
    return jac_ar


def dice_table(vects):
    req_vect = [i[0] for i in vects.values()]
    all_vects = [i for i in vects.values()]
    dice_ar = []
    for vect in vects.values():
        for i in range(len(vect)):
            cur_vect = [k[i] for k in all_vects]
            dice_ar.append(dice(req_vect, cur_vect))
        break
    return dice_ar


path = 'C:\\Users\\Пользователь\\Desktop\\Лаб3 Вект_модель\\collection.txt'
request = "Ученый заявил NASA, что инопанетяне существуют"
if __name__ == "__main__":
    content = txt_reader(path)
    content = txt_parser(content)
    stemmer = RussianStemmer(False)
    stemmed_texts = text_stemmer(content, stemmer)
    tokens = stemmed_tokenizer(stemmed_texts)
    my_dict = bag_of_tokenized(tokens)
    tfidf = get_tf_idf(stemmed_texts, my_dict)
    tokens.append([])
    #vect = bool_tf_tfidf(tokens)[1][' стив ']
    #print(vect)
    request = formating_request(request)
    parsed_request = txt_parser(request)

    stemmed_request = text_stemmer(parsed_request, stemmer)
    for i in stemmed_texts:
        stemmed_request.append(i)

    tokens = stemmed_tokenizer(stemmed_request)
    my_dict = bag_of_tokenized(tokens)
    tokens.append([])
    vect = get_tf_idf(stemmed_request, my_dict)
    #vect = bool_tf_tfidf(tokens)[2]
    sim_cosine_table(vect)
    jaccard_table(vect)
    dice_table(vect)
    index(path)
