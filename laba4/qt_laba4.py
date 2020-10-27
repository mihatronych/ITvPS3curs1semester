import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import csv
from ITvPS.laba4.simplicity_measure import *

class Form(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vect = {}
        self.typeTable = "Boolean VSM"
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))
        self.qTable = QTableWidget(self)
        self.saved_path = ""


        getFileNameButton = QPushButton("Индексирование")
        getFileNameButton.clicked.connect(self.getFileName)

        outTokensButton = QPushButton("Поиск")
        outTokensButton.clicked.connect(self.search)

        self.text_multiline = QPlainTextEdit()

        layoutV = QVBoxLayout()
        layoutV.addWidget(getFileNameButton)
        layoutV.addWidget(outTokensButton)
        layoutV.addWidget(self.text_multiline)

        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addWidget(self.plainTextEdit)
        layoutH.addWidget(self.qTable)
        centerWidget = QWidget()
        centerWidget.setLayout(layoutH)

        #centerWidget = QWidget(self)
        self.setCentralWidget(centerWidget)

        self.qTable.setColumnCount(4)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        headers = []
        headers.append("Текст")
        headers.append("Cosine")
        headers.append("Jaccard")
        headers.append("Dice")
        self.qTable.setHorizontalHeaderLabels(headers)

        # Устанавливаем выравнивание на заголовки
        self.qTable.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight)
        self.qTable.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.resize(1800, 480)
        self.setWindowTitle("PyQt5-laba4-Dolgushin")
        self.plainTextEdit.appendHtml("Приложение запущено!")
        self.plainTextEdit.setReadOnly(True)

    #def getDirectory(self):  # <-----
    #    dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
    #    self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(dirlist))

    def getFileName(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "*.txt")
        self.plainTextEdit.appendHtml("<br>Индексируем файл: <b>{}</b> <br> <b>{:*^54}</b>"
                                      "".format(filename, filetype))
        vect = []
        filename = str(filename)
        print(filename)
        try:
            #print(str.replace(filename, "/", "\\\\"))

            vect = index(filename)
            #table = preprocessing(filename)
            self.qTable.clear()
            headers = []
            headers.append("Текст")
            headers.append("Cosine")
            headers.append("Jaccard")
            headers.append("Dice")
            self.qTable.setHorizontalHeaderLabels(headers)
            self.vect = vect
            self.saved_path = filename
            self.plainTextEdit.appendHtml("<br>Индексирование текста завершено")
        except Exception as e:
            self.plainTextEdit.appendHtml("<br>Ошибка при чтении дока" + str(e))
            self.vect = vect
            self.qTable.clear()
            headers = []
            headers.append("Текст")
            headers.append("Cosine")
            headers.append("Jaccard")
            headers.append("Dice")
            self.qTable.setHorizontalHeaderLabels(headers)
        #print(self.table)

    def search(self):
        try:
            if self.vect != {} and self.saved_path != "":
                self.qTable.clear()
                headers = []
                headers.append("Текст")
                headers.append("Cosine")
                headers.append("Jaccard")
                headers.append("Dice")
                self.qTable.setHorizontalHeaderLabels(headers)
                self.plainTextEdit.appendHtml("<br>Начат поиск по запросу: "+self.text_multiline.toPlainText())
                content = txt_reader(self.saved_path)
                content = txt_parser(content)
                stemmer = RussianStemmer(False)
                stemmed_texts = text_stemmer(content, stemmer)
                request = formating_request(self.text_multiline.toPlainText())
                parsed_request = txt_parser(request)

                stemmed_request = text_stemmer(parsed_request, stemmer)
                for i in stemmed_texts:
                    stemmed_request.append(i)

                tokens = stemmed_tokenizer(stemmed_request)
                tokens.append([])
                vect = bool_tf_tfidf(tokens)[2]
                cos_table = sim_cosine_table(vect)
                jac = jaccard_table(vect)
                dic = dice_table(vect)
                table = []
                for i in range(len(cos_table)):
                    if i == 0:
                        table.append(["Запрос", cos_table[i], jac[i], dic[i]])
                    else:
                        table.append(["Текст" + str((i+1)), cos_table[i], jac[i], dic[i]])

                table.sort(key=lambda i: i[1])
                table.reverse()

                for i in range(len(cos_table)):
                    self.qTable.setRowCount(i + 1)
                    self.qTable.setItem(i, 0, QTableWidgetItem(table[i][0]))
                    self.qTable.setItem(i, 1, QTableWidgetItem(str(table[i][1])))
                    self.qTable.setItem(i, 2, QTableWidgetItem(str(table[i][2])))
                    self.qTable.setItem(i, 3, QTableWidgetItem(str(table[i][3])))


        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Form()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
