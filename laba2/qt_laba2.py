import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from preprocessing_laba_2 import preprocessing
from csv_rw_laba2 import *

class Form(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = []
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))
        self.qTable = QTableWidget(self)


        getFileNameButton = QPushButton("Загрузить текст")
        getFileNameButton.clicked.connect(self.getFileName)

        outTokensButton = QPushButton("Вывести токены")
        outTokensButton.clicked.connect(self.outTokens)

        saveFileNameButton = QPushButton("Сохранить как")
        saveFileNameButton.clicked.connect(self.saveFile)

        layoutV = QVBoxLayout()
        layoutV.addWidget(getFileNameButton)
        layoutV.addWidget(saveFileNameButton)

        radiobutton = QRadioButton("Фильтр по id")
        radiobutton.setChecked(True)
        radiobutton.country = "Фильтр по id"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("Фильтр по алфавиту")
        radiobutton.country = "Фильтр по алфавиту"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        radiobutton = QRadioButton("Фильтр по длине слова")
        radiobutton.country = "Фильтр по длине слова"
        radiobutton.toggled.connect(self.onClicked)
        layoutV.addWidget(radiobutton, 0)

        layoutV.addWidget(outTokensButton)

        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addWidget(self.plainTextEdit)
        layoutH.addWidget(self.qTable)
        centerWidget = QWidget()
        centerWidget.setLayout(layoutH)

        #centerWidget = QWidget(self)
        self.setCentralWidget(centerWidget)

        self.qTable.setColumnCount(5)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.qTable.setHorizontalHeaderLabels(["ID","Token", "No. of document", "Count", "POS"])

        # Устанавливаем выравнивание на заголовки
        self.qTable.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight)
        self.qTable.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.qTable.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.resize(1600, 480)
        self.setWindowTitle("PyQt5-laba2-Dolgushin")

    #def getDirectory(self):  # <-----
    #    dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
    #    self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(dirlist))

    def getFileName(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "CSV files (*.csv)")
        self.plainTextEdit.appendHtml("<br>Выбрали файл: <b>{}</b> <br> <b>{:*^54}</b>"
                                      "".format(filename, filetype))
        table = []
        try:
            #print(str.replace(filename, "/", "\\\\"))
            table = preprocessing(filename)
            self.plainTextEdit.appendHtml("<br>Обработка текста завершена")
        except:
            self.plainTextEdit.appendHtml("<br>Ошибка при предобработке")
        self.table = table
        self.qTable.clear()
        self.qTable.setHorizontalHeaderLabels(["ID", "Token", "No. of document", "Count", "POS"])
        #print(self.table)


    def outTokens(self):
        if self.table != []:
            self.qTable.clear()
            self.qTable.setHorizontalHeaderLabels(["ID", "Token", "No. of document", "Count", "POS"])
            for i in range(len(self.table)):
                if i == 0:
                    heads = str.split(self.table[i],"#")
                else:
                    string = str.split(self.table[i],"#")
                    self.qTable.setRowCount(i)
                    self.qTable.setItem(i - 1, 0, QTableWidgetItem(string[0]))
                    self.qTable.setItem(i - 1, 1, QTableWidgetItem(string[1]))
                    self.qTable.setItem(i - 1, 2, QTableWidgetItem(string[2]))
                    self.qTable.setItem(i - 1, 3, QTableWidgetItem(string[3]))
                    self.qTable.setItem(i - 1, 4, QTableWidgetItem(string[4]))
            self.plainTextEdit.appendHtml("<br>Вывели токены отсортированные по ID")
        else:
            self.plainTextEdit.appendHtml("<br>Выводить нечего")


    def saveFile(self):
        filename, ok = QFileDialog.getSaveFileName(self,
                                                   "Сохранить файл как...",
                                                   "db.csv",
                                                   "CSV files (*.csv)")
        if ok == "CSV files (*.csv)":
            self.plainTextEdit.appendHtml("<br>Сохранить обработанный текст: <b>{}</b> <br> <b>{:*^54}</b>"
                                      "".format(filename, ok))

            if self.table != []:
                data = [i.replace("\\xa0", " ").split("#") for i in self.table]
                print("OK")
                my_list = []
                print(data)
                fieldnames = data[0]
                for values in data[1:]:
                    inner_dict = dict(zip(fieldnames, values))
                    my_list.append(inner_dict)
                path = filename
                csv_dict_writer(path, fieldnames, my_list)
            else:
                print("Ошибка при сохранении")
        else: print("Ошибка при сохранении")

    def sortByAlphabet(self):
        if self.table != []:
            tokens_sorted = [str.split(i, "#") for i in self.table][1:]
            tokens_sorted.sort(key=lambda x: x[1])
            self.qTable.clear()
            self.qTable.setHorizontalHeaderLabels(["ID", "Token", "No. of document", "Count", "POS"])
            for i in range(len(tokens_sorted)):
                self.qTable.setRowCount(i + 1)
                self.qTable.setItem(i, 0, QTableWidgetItem(tokens_sorted[i][0]))
                self.qTable.setItem(i, 1, QTableWidgetItem(tokens_sorted[i][1]))
                self.qTable.setItem(i, 2, QTableWidgetItem(tokens_sorted[i][2]))
                self.qTable.setItem(i, 3, QTableWidgetItem(tokens_sorted[i][3]))
                self.qTable.setItem(i, 4, QTableWidgetItem(tokens_sorted[i][4]))
            self.plainTextEdit.appendHtml("<br>Отсортировали по алфавиту")
        else:
            self.plainTextEdit.appendHtml("<br>Сортировать нечего нечего")

    def sortByWordLength(self):
        if self.table != []:
            tokens_sorted = [str.split(i, "#") for i in self.table][1:]
            tokens_sorted.sort(key=lambda x: len(x[1]))
            self.qTable.clear()
            self.qTable.setHorizontalHeaderLabels(["ID", "Token", "No. of document", "Count", "POS"])
            for i in range(len(tokens_sorted)):
                self.qTable.setRowCount(i + 1)
                self.qTable.setItem(i, 0, QTableWidgetItem(tokens_sorted[i][0]))
                self.qTable.setItem(i, 1, QTableWidgetItem(tokens_sorted[i][1]))
                self.qTable.setItem(i, 2, QTableWidgetItem(tokens_sorted[i][2]))
                self.qTable.setItem(i, 3, QTableWidgetItem(tokens_sorted[i][3]))
                self.qTable.setItem(i, 4, QTableWidgetItem(tokens_sorted[i][4]))
            self.plainTextEdit.appendHtml("<br>Отсортировали по длине слов")
        else:
            self.plainTextEdit.appendHtml("<br>Сортировать нечего нечего")

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Country is %s" % (radioButton.country))
            if radioButton.country == "Фильтр по id":
                self.outTokens()
                print(" ")
            if radioButton.country == "Фильтр по алфавиту":
                self.sortByAlphabet()
                print(" ")
            if radioButton.country == "Фильтр по длине слова":
                self.sortByWordLength()
                print(" ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())