#clase para los afd
import json
class Afd:
    #constructor
    def __init__(self):
        self.dataDirAFD1="./ENTRADA/data_AFD_1.json"
        self.dataDirAFD2="./ENTRADA/data_AFD_2.json"
        self.dataAFD1={}
        self.dataAFD2={}
    
    def leerAFD(self):
        with open(self.dataDirAFD1, mode='r', encoding="utf-8") as jsonFile:
            self.dataAFD1 = json.load(jsonFile)
        with open(self.dataDirAFD2, mode='r', encoding="utf-8") as jsonFile:
            self.dataAFD2 = json.load(jsonFile)
    
    def escribirAFD(self):
        with open(self.dataDirAFD1, mode='w', encoding="utf-8") as jsonFile:
            json.dump(self.dataAFD1, jsonFile, ensure_ascii=False)
        with open(self.dataDirAFD2, mode='w', encoding="utf-8") as jsonFile:
            json.dump(self.dataAFD2, jsonFile, ensure_ascii=False)