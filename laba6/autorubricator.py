import os
import re
import pymystem3 as Stem
import math
import csv
from nltk.corpus import stopwords

#Допилить F1

def checkExecTimeMystemOneText(texts):
    lol = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
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
                    doc.append(" " + txt + " ")
        return res


def del_of_spec_symbols(content):
    s = str(content)
    s = re.sub('[^A-Za-zА-Яа-я ё]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    stopWords = set(stopwords.words('english'))
    s = str.lower(s)
    for sw in stopWords:
        if s.split(" ").count(sw) > 0:
           s = s.replace(" "+sw+" ", " ")
    return s


def bag_of_tokenized(tokens):
    bag_of_words = set()
    for i in tokens:
        some_set = set(i)
        bag_of_words.update(some_set)
    return bag_of_words


def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    data = ["title;keywords;annotation;class"]
    data_splitted = []
    vect_table = {}
    for line in reader:
        f = line.keys()
        string = "{};{};{};{}".format(line["п»їtitle"], line["keywords"], line["annotation"], line["class"])
        data.append(string)
        data_splitted.append(str.split(string, ";"))
        vect_table[str.split(string, ";")[0]] = str.split(string, ";")[1:]
    return vect_table


def group_classes(tokens, uber_table):
    classes = [[], [], [], []]
    vals = list(uber_table.values())
    for i in range(len(tokens)):
        if str(vals[i][-1]) == "1":
            classes[0].append(tokens[i])
        if str(vals[i][-1]) == "2":
            classes[1].append(tokens[i])
        if str(vals[i][-1]) == "3":
            classes[2].append(tokens[i])
        if str(vals[i][-1]) == "4":
            classes[3].append(tokens[i])
    return classes


def count_w_in_cs(bag_of_tokenized, classes):
    res = {}
    for w in bag_of_tokenized:
        c = []
        for clas in classes:
            count = 0
            for doc in clas:
                count += doc.count(w)
            c.append(count)
        res[w] = c
    return res


def count_wc_in_cs(tf, bag, classes):
    res = {}
    for w in bag:
        wcs = []
        for i in range(len(classes)):
            count_c = 0
            for doc in classes[i]:
                count_c += len(doc)
            wc = (tf[w][i] + 1) / (count_c + len(bag))
            wcs.append(wc)
        res[w] = wcs
    return res


def uber_table_write_in_csv(uber_table):
    data = ["term,c1,c2,c3,c4,pwc1,pwc2,pwc3,pwc4,pc1,pc2,pc3,pc4".split(",")]
    for el in uber_table.items():
        data.append([el[0]] + el[1])

    my_list = []
    fieldnames = data[0]
    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)

    path = "trained.csv"
    csv_dict_writer(path, fieldnames, my_list)


def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def csv_trained_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    data = ["term;c1;c2;c3;c4;pwc1;pwc2;pwc3;pwc4;pc1;pc2;pc3;pc4"]
    data_splitted = []
    vect_table = {}
    for line in reader:
        f = line
        string = "{};{};{};{};{};{};{};{};{};{};{};{};{}".format(line["term"], line["c1"], line["c2"], line["c3"],
                                                                 line["c4"], line["pwc1"], line["pwc2"], line["pwc3"],
                                                                 line["pwc4"], line["pc1"], line["pc2"], line["pc3"],
                                                                 line["pc4"])
        data.append(string)
        data_splitted.append(str.split(string, ";"))
        vect_table[str.split(string, ";")[0]] = str.split(string, ";")[1:]
    return vect_table


def classes_write_in_txt(classes_from_texts):
    with open("classes.txt", 'w', encoding='utf-8') as f_obj:
        for i in range(len(classes_from_texts)):
            docs = ""
            for doc in classes_from_texts[i]:
                docs += "#" + "#".join(doc)
            f_obj.write("\r\nclass" + docs)

def extract_features(message, wf):
    message_words = set(message)
    features = {}
    for word in wf:
        features['contains(%s)' % word] = (word in message_words)
    return features

def train_rubricator(path):
    with open(path) as f_obj:
        uber_table = csv_dict_reader(f_obj)
    tokens = checkExecTimeMystemOneText([del_of_spec_symbols(i) for i in uber_table.values()])
    bag = bag_of_tokenized(tokens)
    classes = group_classes(tokens, uber_table)
    classes_write_in_txt(classes)
    tf = count_w_in_cs(bag, classes)
    wc_table = count_wc_in_cs(tf, bag, classes)
    pc = []
    for i in range(len(classes)):
        pc.append(len(classes[i]))
    train_tutu = {}
    for w in bag:
        train_tutu[w] = tf[w] + wc_table[w] + pc
    uber_table_write_in_csv(train_tutu)


def classes_read_from_txt():
    classes = []
    with open("classes.txt", 'r', encoding='utf-8') as f_obj:
        p = ""
        for lines in f_obj:
            p = lines
            if lines != "\n":
                classes.append(lines.split("#")[1:])

    c = len(classes)
    return classes


def find_pcd(ppr_doc, c_num, uber_mega_table):
    p_of_c = [i for i in uber_mega_table.values()][0][-4:]
    p_of_c = [int(i) for i in p_of_c]
    pcd = math.log2(p_of_c[c_num - 1] / (p_of_c[0] + p_of_c[1] + p_of_c[2] + p_of_c[3]))
    for w in ppr_doc:
        if uber_mega_table.__contains__(w):
            pcd += math.log2(float(uber_mega_table[w][c_num - 1 + 4]))
    return pcd


def raw_classificate(doc, uber_mega_table):
    t = del_of_spec_symbols(doc[0]) + "".join([del_of_spec_symbols(i) for i in doc[1]])
    ppr_doc = checkExecTimeMystemOneText([del_of_spec_symbols(t)])[0]
    return [find_pcd(ppr_doc, 1, uber_mega_table), \
           find_pcd(ppr_doc, 2, uber_mega_table), \
           find_pcd(ppr_doc, 3, uber_mega_table), \
           find_pcd(ppr_doc, 4, uber_mega_table)]


if __name__ == "__main__":
    path = "train.csv"
    train_rubricator(path)
    with open("trained.csv") as f_obj:
        uber_table = csv_trained_reader(f_obj)
    with open("test.csv") as f_obj:
        test = csv_dict_reader(f_obj)
    test_clas = []
    for i in test.items():
        test_clas.append(raw_classificate(i, uber_table))
        #print(raw_classificate(i, uber_table))
    f_t = {}
    c = 0
    print(list(test.values())[0])
    test_vals = list(test.values())
    tp1 = 0
    fp1 = 0
    fn1 = 0
    tp2 = 0
    fp2 = 0
    fn2 = 0
    tp3 = 0
    fp3 = 0
    fn3 = 0
    tp4 = 0
    fp4 = 0
    fn4 = 0
    for i in test_clas:
        c += 1
        mx = max(i)
        cl = 0
        if mx == i[0]:
            cl = 1
        if mx == i[1]:
            cl = 2
        if mx == i[2]:
            cl = 3
        if mx == i[3]:
            cl = 4
        f_t[c] = i, cl, int(test_vals[c - 1][-1])
        if cl == int(test_vals[c - 1][-1]):
            if cl == 1:
                tp1 += 1
            if cl == 2:
                tp2 += 1
            if cl == 3:
                tp3 += 1
            if cl == 4:
                tp4 += 1
        else:
            if cl == 1:
                fp1 += 1
            if cl == 2:
                fp2 += 1
            if cl == 3:
                fp3 += 1
            if cl == 4:
                fp4 += 1
            if int(test_vals[c - 1][-1]) == 1:
                fn1 += 1
            if int(test_vals[c - 1][-1]) == 2:
                fn2 += 1
            if int(test_vals[c - 1][-1]) == 3:
                fn3 += 1
            if int(test_vals[c - 1][-1]) == 4:
                fn4 += 1
    print("num " + str(1) + " " + str(2) + " " + str(3) + " " + str(4))
    print("tp "+ str(tp1) + " " + str(tp2) + " " +str(tp3) + " " +str(tp4))
    print("fp " + str(fp1) + " " + str(fp2) + " " + str(fp3) + " " + str(fp4))
    print("fn " + str(fn1) + " " + str(fn2) + " " + str(fn3) + " " + str(fn4))
    print(f_t)
    F11 = 0
    F12 = 0
    F13 = 0
    F14 = 0
    P1 = 0
    P2 = 0
    P3 = 0
    P4 = 0
    R1 = 0
    R2 = 0
    R3 = 0
    R4 = 0
    if (tp1 + fp1 != 0 and tp1 + fn1 != 0):
        P1 = tp1 / (tp1 + fp1)
        R1 = tp1 / (tp1 + fn1)
        F11 = 2 * P1 * R1 / (P1 + R1)
    if(tp2 + fp2 != 0 and tp2 + fn2 != 0):
        P2 = tp2 / (tp2 + fp2)
        R2 = tp2 / (tp2 + fn2)
        F12 = 2 * P2 * R2 / (P2 + R2)
    if (tp3 + fp3 != 0 and tp3 + fn3 != 0):
        P3 = tp3 / (tp3 + fp3)
        R3 = tp3 / (tp3 + fn3)
        F13 = 2 * P3 * R3 / (P3 + R3)
    if (tp4 + fp4 != 0 and tp4 + fn4 != 0):
        P4 = tp4 / (tp4 + fp4)
        R4= tp4 / (tp4 + fn4)
        F14 = 2 * P4 * R4 / (P4 + R4)
    print(P1, R1, F11)
    print(P2, R2, F12)
    print(P3, R3, F13)
    print(P4, R4, F14)
