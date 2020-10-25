import re
import sys
import pymorphy2
import array
import math
from nltk.stem.snowball import RussianStemmer
from preprocessing_laba_2 import del_of_spec_symbols, checkExecTimeMystemOneText

def txt_reader(path):
    content = ""
    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read()
    return content

def txt_parser(content):
    pattern = "[Д][о][к][у][м][е][н][т][ ][№][ ]{0,1}[\d]{1,3}[*]{40,44}"
    cont_docs = re.split(pattern, content)
    return cont_docs

def txt_tokenizer(cont_docs):
    cont_docs = del_of_spec_symbols(cont_docs)
    tokens = checkExecTimeMystemOneText(cont_docs)
    return tokens

def text_stemmer(content, stemmer):
    content = del_of_spec_symbols(content)
    ar_stem = []
    temp = []
    for i in content:
        temp = []
        ar =i.split(" ")
        for k in ar:
            if k!="":
                temp.append(stemmer.stem(k))
        if temp != []:
            ar_stem.append(temp)
    return ar_stem

def bag_of_tokenized(tokens):
    bag_of_words = set()
    for i in tokens:
        some_set = set(i)
        bag_of_words.update(some_set)
    return bag_of_words

def bool_tf_tfidf(tokens):
    bag_of_words = bag_of_tokenized(tokens)
    d = {}
    boolean = {}
    tf = {}
    tfidf = {}
    Nd = len(tokens)  # кол-во док-тов
    for i in bag_of_words:
        b = []
        c = []
        ti = []
        t = 0  # Это др. tf
        N = 0  # Это число док-тов содержащих слово
        for k in range(len(tokens) - 1):
            ar = []
            ar.extend(tokens[k])
            ar.__contains__(i)
            b.append(1 if ar.__contains__(i) else 0)
            c.append(ar.count(i))
            N = N + 1 if ar.__contains__(i) else N

        for k in range(len(tokens)):
            ar = []
            ar.extend(tokens[k])
            if len(ar) != 0:
                t = ar.count(i) / len(ar)
                ti.append(t * math.log2(Nd / N))
        boolean[i] = b
        tf[i] = c
        tfidf[i] = ti
    res = []
    res.append(boolean)
    res.append(tf)
    res.append(tfidf)
    return res

def get_bag_of_stemmed_words(stemmed_text):
    bag_of_words = set()
    for i in stemmed_text:
        some_set = set(i)
        bag_of_words.update(some_set)
    return bag_of_words

def get_bag_of_bigramms(stemmed_text):
    bag_of_bigramms = set()
    for doc in stemmed_text:
        for i in range(len(doc)):
            if i + 1 < len(doc):
                bag_of_bigramms.add(doc[i] + " " + doc[i + 1])
    return bag_of_bigramms

def get_bag_of_trigramms(stemmed_text):
    bag_of_trigramms = set()
    for doc in stemmed_text:
        for i in range(len(doc)):
            if i + 2 < len(doc):
                bag_of_trigramms.add(doc[i] + " " + doc[i + 1] + " " + doc[i + 2])
    return bag_of_trigramms

def get_unigram(stemmed_text):
    bag_of_words = get_bag_of_stemmed_words(stemmed_text)
    unigram = {}
    for i in bag_of_words:
        c = []
        for k in stemmed_text:
            c.append(k.count(i))
        unigram[i] = c
    return unigram

def get_bigram(stemmed_text):
    bag_of_bigramms = get_bag_of_bigramms(stemmed_text)
    bigram = {}
    for i in bag_of_bigramms:
        c = []
        for k in stemmed_text:
            temp = " ".join(k)
            c.append(temp.count(i))
        bigram[i] = c
    return bigram

def get_trigram(stemmed_text):
    bag_of_trigramms = get_bag_of_trigramms(stemmed_text)
    trigram = {}
    for i in bag_of_trigramms:
        c = []
        for k in stemmed_text:
            temp = " ".join(k)
            c.append(temp.count(i))
        trigram[i] = c
    return trigram

path = 'C:\\Users\\Пользователь\\Desktop\\Лаб3 Вект_модель\\collection.txt'

if __name__ == "__main__":
    content = txt_reader(path)
    content = txt_parser(content)
    tokens = txt_tokenizer(content)
    some_vectores = bool_tf_tfidf(tokens)
    stemmer = RussianStemmer(False)
    stemmed_texts = text_stemmer(content, stemmer)
    boolean = some_vectores[0]
    tf = some_vectores[1]
    tfidf = some_vectores[2]
    unigram = get_unigram(stemmed_texts)
    bigram = get_bigram(stemmed_texts)
    trigram = get_trigram(stemmed_texts)

    list_d = list(unigram.items())
    list_d.sort(key=lambda i: i[1][0])
    list_d.reverse()
    for i in range(10):
        print(list_d[i])

