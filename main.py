import typing
from PyQt5.QtWidgets import QLabel,QSpinBox,QLayout,QApplication,QMainWindow,QPushButton, QWidget
from PyQt5 import QtCore, uic
import sys
import pymongo
import json
import random
connection = pymongo.MongoClient("localhost",27017)
database = connection["N5"]
kanjis = database["kanjis"]


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        self.app_main = app_life()
        uic.loadUi("mainUI.ui",self)
        self.show()
        self.CharShowed = False
        self.kanji_toshow ={}
        self.mainKanji: QLabel = self.findChild(QLabel,"mainKanji")
        self.yomis :QLabel = self.findChild(QLabel,"yomis")
        self.random_btn :QPushButton = self.findChild(QPushButton,"Random_btn")
        self.see_btn :QPushButton = self.findChild(QPushButton,"see_btn")
        self.vocabs : QLabel = self.findChild(QLabel,"Vocabs")
        self.spinBox : QSpinBox = self.findChild(QSpinBox,"grade")
        self.spinBox.setRange(1,10)
        self.strokes : QLabel = self.findChild(QLabel,"stroke")
        ##functions
        self.random_btn.clicked.connect(lambda : self.handle_kanji(int(self.spinBox.value())))
        self.see_btn.clicked.connect(lambda : self.handle_vocabs(self.kanji_toshow))
    
    def handle_kanji(self,level:int):
        if level == 7:
            self.kanji_toshow = self.app_main.showKnaji(level - 1)
        else:
            self.kanji_toshow = self.app_main.showKnaji(level)
            #print(self.kanji_toshow)
        self.CharShowed = True
        self.yomis.setText(" ")
        self.vocabs.setText(" ")
        self.strokes.setText(" ")
        self.main_key = next(iter(self.kanji_toshow))
        self.mainKanji.setText(str(self.main_key))
    def bracket_remover(self,data):
        new_data = ""
        for i in str(data):
            if i == "[" or "]":
                i == " "
                new_data += i
            else:
                new_data += i
        return new_data

    def handle_vocabs(self,data):
        if self.CharShowed == True:
            oun =  self.bracket_remover(str(data[self.main_key]["readings_on"]) )
            kun = self.bracket_remover(str(data[self.main_key]["readings_kun"]))
            stroks_data = str(data[self.main_key]["strokes"])
            yomis = "Oun : " + oun +"      "+ "Kun : " + kun
            meaning = str(data[self.main_key]["meanings"])
            self.yomis.setText(yomis)
            self.vocabs.setText(meaning)
            self.strokes.setText("Strokes : " + stroks_data)
        
            

class app_life():
    def __init__(self):
        
        with open("kanji-wanikani.json","r", encoding='utf-8') as data:
            self.kanji_data = json.load(data)
    


    def fetch_kanji(self,specific_value : int):
        req_data = {}
        index = 0
        for key,value in self.kanji_data.items():
            if value["grade"] == specific_value:
                req_data.update({index:{key:value}})
                index += 1

        #print(req_data)
        return req_data

    def randomMize_data(self,kanjis: dict):
        print(len(kanjis))
        random_num = random.randint(0,len(kanjis))
        #print(random_num)
        return random_num
    
    def showKnaji(self,level : int):
        kanjis = self.fetch_kanji(int(level))
        randomNum = self.randomMize_data(kanjis)
        return kanjis[randomNum]
        #print(kanjis[randomNum])
   

app= QApplication(sys.argv)
window = UI()
window.setWindowTitle("Kanji No Benkyou")
sys.exit(app.exec())