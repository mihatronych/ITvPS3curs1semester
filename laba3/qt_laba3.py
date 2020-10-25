import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from vectoriser_laba_3 import txt_reader, txt_parser, txt_tokenizer, bool_tf_tfidf, text_stemmer, get_unigram, get_bigram, get_trigram
from nltk.stem.snowball import RussianStemmer
import csv

class Form(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = []
        self.typeTable = "Boolean VSM"
        self.VSM = {}
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))
        self.qTable = QTableWidget(self)


        getFileNameButton = QPushButton("Выбрать текст (корпус)")
        getFileNameButton.clicked.connect(self.getFileName)

        outTokensButton = QPushButton("Построить модель")
        outTokensButton.clicked.connect(self.createModel)

        showButton = QPushButton("Показать результаты")
        showButton.clicked.connect(self.outTable)

        saveFileNameButton = QPushButton("Сохранить как")
        saveFileNameButton.clicked.connect(self.saveFile)

        layoutV = QVBoxLayout()
        layoutV.addWidget(getFileNameButton)
        layoutV.addWidget(saveFileNameButton)
        layoutV.addWidget(outTokensButton)
        layoutV.addWidget(showButton)
        radiobutton = QRadioButton("Boolean VSM")
        radiobutton.setChecked(True)
        radiobutton.country = "Boolean VSM"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("TF VSM")
        radiobutton.country = "TF VSM"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("TF-IDF VSM")
        radiobutton.country = "TF-IDF VSM"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("Униграмма")
        radiobutton.country = "Униграмма"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("Биграмма")
        radiobutton.country = "Биграмма"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("Триграмма")
        radiobutton.country = "Триграмма"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)


        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addWidget(self.plainTextEdit)
        layoutH.addWidget(self.qTable)
        centerWidget = QWidget()
        centerWidget.setLayout(layoutH)

        #centerWidget = QWidget(self)
        self.setCentralWidget(centerWidget)

        self.qTable.setColumnCount(11)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        headers = []
        for i in range(11):
            if i == 0:
                headers.append("Term")
            else:
                headers.append("Текст_"+str(i))
        self.qTable.setHorizontalHeaderLabels(headers)

        # Устанавливаем выравнивание на заголовки
        self.qTable.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight)
        self.qTable.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.resize(1800, 480)
        self.setWindowTitle("PyQt5-laba2-Dolgushin")

    #def getDirectory(self):  # <-----
    #    dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
    #    self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(dirlist))

    def getFileName(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "*.txt")
        self.plainTextEdit.appendHtml("<br>Выбрали файл: <b>{}</b> <br> <b>{:*^54}</b>"
                                      "".format(filename, filetype))
        table = []
        filename = str(filename)
        print(filename)
        try:
            #print(str.replace(filename, "/", "\\\\"))

            table = txt_reader(filename)
            table = txt_parser(table)
            #table = preprocessing(filename)
            headers = []
            for i in range(len(table) + 1):
                if i == 0:
                    headers.append("Term")
                else:
                    headers.append("Текст_" + str(i))
            self.table = table
            self.qTable.clear()
            self.qTable.setHorizontalHeaderLabels(headers)
            self.plainTextEdit.appendHtml("<br>Обработка текста завершена")
        except Exception as e:
            self.plainTextEdit.appendHtml("<br>Ошибка при чтении дока" + str(e))
            self.table = table
            self.qTable.clear()
        #print(self.table)


    def createModel(self):
        if self.table != []:
            self.qTable.clear()
            headers = []
            for i in range(len(self.table) + 1):
                if i == 0:
                    headers.append("Term")
                else:
                    headers.append("Текст_" + str(i))
            self.qTable.setHorizontalHeaderLabels(headers)
            try:
                if self.typeTable == "Boolean VSM":
                    self.outBoolean()
                if self.typeTable == "TF VSM":
                    self.outTF()
                if self.typeTable == "TF-IDF VSM":
                    self.outTFIDF()
                if self.typeTable == "Униграмма":
                    self.outUnigramma()
                if self.typeTable == "Биграмма":
                    self.outBigramma()
                if self.typeTable == "Триграмма":
                    self.outTrigramma()
                self.plainTextEdit.appendHtml("<br>Построили модель типа " + self.typeTable)
            except Exception as e:
                print(str(e))
        else:
            self.plainTextEdit.appendHtml("<br>Ошибочка на выводе")

    def outBoolean(self):
        tokens = txt_tokenizer(self.table)
        some_vectores = bool_tf_tfidf(tokens)
        self.VSM = some_vectores[0]

    def outTF(self):
        tokens = txt_tokenizer(self.table)
        some_vectores = bool_tf_tfidf(tokens)
        self.VSM = some_vectores[1]

    def outTFIDF(self):
        tokens = txt_tokenizer(self.table)
        some_vectores = bool_tf_tfidf(tokens)
        self.VSM = some_vectores[2]

    def outUnigramma(self):
        stemmer = RussianStemmer(False)
        stemmed_texts = text_stemmer(self.table, stemmer)
        unigram = get_unigram(stemmed_texts)
        self.VSM = unigram

    def outBigramma(self):
        stemmer = RussianStemmer(False)
        stemmed_texts = text_stemmer(self.table, stemmer)
        bigram = get_bigram(stemmed_texts)
        self.VSM = bigram

    def outTrigramma(self):
        stemmer = RussianStemmer(False)
        stemmed_texts = text_stemmer(self.table, stemmer)
        trigram = get_trigram(stemmed_texts)
        self.VSM = trigram

    def outTable(self):
        try:
            if self.VSM != {} and self.table != []:
                self.qTable.clear()
                headers = []
                for i in range(len(self.table) + 1):
                    if i == 0:
                        headers.append("Term")
                    else:
                        headers.append("Текст_" + str(i))
                self.qTable.setHorizontalHeaderLabels(headers)

                list_d = list(self.VSM.items())
                list_d.sort(key=lambda i: i[1][0])
                list_d.reverse()
                for i in range(30):
                    self.qTable.setRowCount(i + 1)
                    for t in range(2):
                        if t == 0:
                            self.qTable.setItem(i, t, QTableWidgetItem(list_d[i][t]))
                        else:
                            #for k in range(len(self.table) - 1):
                            for k in range(10):
                                print(str(list_d[i][t][k]))
                                self.qTable.setItem(i, t + k, QTableWidgetItem(str(list_d[i][t][k])))
        except Exception as e:
            print(str(e))



    def saveFile(self):
        filename, ok = QFileDialog.getSaveFileName(self,
                                                   "Сохранить файл как...",
                                                   "db.csv",
                                                   "*.csv")
        if ok == "*.csv":
            self.plainTextEdit.appendHtml("<br>Сохранить обработанный вектор: <b>{}</b> <br> <b>{:*^54}</b>"
                                      "".format(filename, ok))

            if self.table != [] and self.VSM != {}:
                print(list(self.VSM.items()))
                try:
                    print(list(self.VSM.items())[0])
                    data = [i for i in list(self.VSM.items())]
                    print("OK")
                    my_list = []
                    headers = []
                    for i in range(len(self.table)):
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
                    path = filename
                    self.csv_dict_writer(path, fieldnames, my_list)
                except Exception as e:
                    print(str(e))
            else:
                print("Ошибка при сохранении")
        else: print("Ошибка при сохранении")

    def csv_dict_writer(self, path, fieldnames, data):
        """
        Writes a CSV file using DictWriter
        """
        with open(path, "w", encoding='utf8', newline='') as out_file:
            writer = csv.DictWriter(out_file, delimiter='#', fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Country is %s" % (radioButton.country))
            if radioButton.country == "Boolean VSM":
                #self.outTokens()
                self.typeTable = "Boolean VSM"
                print(" ")
            if radioButton.country == "TF VSM":
                self.typeTable = "TF VSM"
                #self.sortByAlphabet()
                print(" ")
            if radioButton.country == "TF-IDF VSM":
                #self.sortByWordLength()
                self.typeTable = "TF-IDF VSM"
                print(" ")
            if radioButton.country == "Униграмма":
                # self.sortByWordLength()
                self.typeTable = "Униграмма"
            if radioButton.country == "Биграмма":
                # self.sortByWordLength()
                self.typeTable = "Биграмма"
            if radioButton.country == "Триграмма":
                # self.sortByWordLength()
                self.typeTable = "Триграмма"

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Form()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))