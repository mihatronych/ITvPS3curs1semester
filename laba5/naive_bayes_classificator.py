import os
import re
import pymystem3 as Stem
import math
import csv

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
    s = str(content)
    s = re.sub('[^A-Za-zА-Яа-я ё]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    s = str.lower(s)
    return s


def txt_reader(path):
    tutu = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            pathh = os.path.join(path, file)
            with open(pathh, encoding='utf-8') as f_obj:
                tutu.append(f_obj.read())
    return tutu

def bag_of_tokenized(tokens):
    bag_of_words = set()
    for i in tokens:
        some_set = set(i)
        bag_of_words.update(some_set)
    return bag_of_words

def count_w_in_cs(bag_of_tokenized, classes):
    res = {}
    for w in bag_of_tokenized:
        c = []
        for clas in classes:
            c.append(clas.count(w))
        res[w] = c
    return res

def count_wc_in_cs(c_table, bag, classes):
    res = {}
    for w in bag:
        wcs = []
        for i in range(len(classes)):
            wc = (c_table[w][i] + 1) / (len(classes[i]) + len(bag))
            wcs.append(wc)
        res[w] = wcs
    return res


def get_table_trained(path):
    tutu = txt_reader(path)
    ppr = checkExecTimeMystemOneText([del_of_spec_symbols(i) for i in tutu])
    bag = bag_of_tokenized(ppr)
    classes_from_texts = [ppr[i] + ppr[i + 1] + ppr[i + 2] for i in range(0, len(ppr), 3)]
    c_table = count_w_in_cs(bag, classes_from_texts)
    wc_table = count_wc_in_cs(c_table, bag, classes_from_texts)
    uber_table = {}
    for w in bag:
        uber_table[w] = c_table[w] + wc_table[w]

    return uber_table

def retrain(doc, bag, classes,c_num, p_of_c):
    ppr_doc = checkExecTimeMystemOneText([del_of_spec_symbols(doc)])
    bag.update(bag_of_tokenized(ppr_doc))
    classes[c_num-1] += ppr_doc[0]
    classes_write_in_txt(classes)
    c_table = count_w_in_cs(bag, classes)
    wc_table = count_wc_in_cs(c_table, bag, classes)
    uber_table = {}
    for w in bag:
        uber_table[w] = c_table[w] + wc_table[w]
    p_of_c[c_num-1] += 1
    p_of_c_write_in_txt(p_of_c)
    uber_table_write_in_csv(uber_table)
    return uber_table

def find_pcd(ppr_doc, c_num, uber_mega_table, p_of_c):
    pcd = math.log2(p_of_c[c_num-1]/(p_of_c[0] + p_of_c[1] + p_of_c[2]))
    for w in ppr_doc:
        if uber_mega_table.__contains__(w):
            pcd += math.log2(float(uber_mega_table[w][c_num-1 + 3]))
    return pcd

def raw_classificate(doc, uber_mega_table):
    ppr_doc = checkExecTimeMystemOneText([del_of_spec_symbols(doc)])[0]
    p_of_c = p_of_c_read_from_txt()
    return [find_pcd(ppr_doc, 1, uber_mega_table, p_of_c), find_pcd(ppr_doc, 2, uber_mega_table, p_of_c), find_pcd(ppr_doc, 3, uber_mega_table, p_of_c)]

def classes_write_in_txt(classes_from_texts):
    with open("classes.txt", 'w', encoding='utf-8') as f_obj:
        for i in range(len(classes_from_texts)):
            f_obj.write("\r\nclass#"+"#".join(classes_from_texts[i]))

def classes_read_from_txt():
    classes = []
    with open("classes.txt", 'r', encoding='utf-8') as f_obj:
        p = ""
        for lines in f_obj:
            p = lines
            if lines !="\n":
                classes.append(lines.split("#")[1:])

    c =len(classes)
    return classes

def p_of_c_write_in_txt(p_of_c):
    with open("p_of_c.txt", 'w', encoding='utf-8') as f_obj:
        for i in range(len(p_of_c)):
            f_obj.write("\r\nclass#"+str(p_of_c[i]))


def p_of_c_read_from_txt():
    p_of_c = []
    with open("p_of_c.txt", 'r', encoding='utf-8') as f_obj:
        for lines in f_obj:
            if lines!= "\n":
                p_of_c.append(int(lines.split("#")[1]))
    return p_of_c

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, delimiter='#', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def uber_table_write_in_csv(uber_table):
    data = ["term,c1,c2,c3,pwc1,pwc2,pwc3".split(",")]
    for el in uber_table.items():
        data.append([el[0]] + el[1])

    my_list = []
    fieldnames = data[0]
    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)

    path = "trained.csv"
    csv_dict_writer(path, fieldnames, my_list)

def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter='#')
    data = ["term#c1#c2#c3#pwc1#pwc2#pwc3"]
    data_splitted = []
    vect_table = {}
    for line in reader:
        f =line
        string = "{}#{}#{}#{}#{}#{}#{}".format(line["term"], line["c1"], line["c2"], line["c3"], line["pwc1"], line["pwc2"], line["pwc3"])
        data.append(string)
        data_splitted.append(str.split(string, "#"))
        vect_table[str.split(string, "#")[0]] = str.split(string, "#")[1:]
    return vect_table

if __name__ == "__main__":
    tutu = txt_reader("C:/Program Files/PycharmProjects/new/venv/ITvPS/laba5/train")
    ppr = checkExecTimeMystemOneText([del_of_spec_symbols(i) for i in tutu])
    bag = bag_of_tokenized(ppr)
    classes_from_texts = [ppr[i] + ppr[i + 1] + ppr[i + 2] for i in range(0, len(ppr), 3)]
    classes_write_in_txt(classes_from_texts)
    c_table = count_w_in_cs(bag, classes_from_texts)
    wc_table = count_wc_in_cs(c_table, bag, classes_from_texts)
    p_of_c = [3, 3, 3]
    p_of_c_write_in_txt(p_of_c)
    uber_table = {}
    for w in bag:
        uber_table[w] = c_table[w] + wc_table[w]
    uber_table_write_in_csv(uber_table)
    while True:
        with open("trained.csv", encoding='utf-8') as f_obj:
            uber_table = csv_dict_reader(f_obj)
        bag = set(uber_table.keys())
        classes = classes_read_from_txt()
        p_of_c = p_of_c_read_from_txt()
        print("Запустить в режиме 'Обучение классификатора'[0] или в режиме 'Определение класса документа'[1]")
        ans = int(input())
        if ans == 0:
            print("Режим 'Обучение классификатора'")
            print("Вставьте текст")
            txt = input()
            inputted = txt
            while inputted != "end":
                inputted = input()
                txt += inputted
            print("Какому классу принадлежит текст? (1-3)")
            c_num = int(input())
            retrain(txt, bag, classes, c_num, p_of_c)
            print("Классификатор успешно дообучен")
        elif ans == 1:
            print("Режим 'Определение класса документа'")
            print("Вставьте текст")
            txt = input()
            inputted = txt
            while inputted != "end":
                inputted = input()
                txt += inputted
            res = raw_classificate(txt, uber_table)
            print("P(c1|d) = " + str(res[0]))
            print("P(c2|d) = " + str(res[1]))
            print("P(c3|d) = " + str(res[2]))
            st = "Документ принадлежит классу "
            print(st + "1") if max(res) == res[0] else print(st + "2") if max(res) == res[1] else print(st + "3")


    #p_of_c = [3, 3, 3]
    #p_of_c_write_in_txt(p_of_c)
    #print(uber_table)
    #new_text = txt_reader("C:/Program Files/PycharmProjects/new/venv/ITvPS/laba5/test")[0]
    ##print(new_text)
    #uber_mega_table = retrain(new_text, bag, classes_read_from_txt(), 1, p_of_c_read_from_txt())
    #print(uber_mega_table)
    #uber_table = []
    #with open("trained.csv", encoding='utf-8') as f_obj:
    #    uber_table = csv_dict_reader(f_obj)
    #test = txt_reader("C:/Program Files/PycharmProjects/new/venv/ITvPS/laba5/test")[1]
    #print(raw_classificate(test, uber_table))
