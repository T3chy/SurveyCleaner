from datetime import datetime as dt
import re
import math
import numpy as np
import pandas as pd
import parsejobs
pd.options.display.max_rows = 999
surveyDefaultBinaryQs = ["QID81 - ¿Está empleada/o actualmente?", "¿Sabe Usted lo que son las pruebas genéticas?", "¿Te has hecho una prueba genética alguna vez?", "Exámen de seno / Mamografía", "Exámen cervical / Papanicolao", "Exámen colorectal / Colonoscopía"]
surveyDefaultNumericQs = ["Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?", "QID80 - ¿Cuántas personas viven con Usted?"]
id = "Por favor complete con sus datos: - Número de identificación del estudio"
post = "Por favor complete con sus datos: - Código Postal"

jobs = parsejobs.parseJobsTxt("jobs.txt")
class survey:
    def __init__(self,name):
        self.name = name.strip(".xlsx")
        self.read = pd.read_excel(name, engine="openpyxl")
        self.merged = ""
        self.data = self.read.copy()
        self.changes = []
        self.flagged = []
        self.index = 0
        self.q = ""
    def logChange(self, qtype, init, reason=""):
        final = self.data.loc[self.index,self.q]
        rid = self.data.loc[self.index,id]
        if str(init).lower().strip("'") != str(final).lower().strip("'"):
            if final == "":
                final = "an empty string"
            self.changes.append(str(qtype).upper() + ": Replaced " + str(init) + " with " + str(final) + " at respondant with ID " + str(rid)+ " question " + str(self.q) + " " + reason)

    def validID(self,tmp, log=True):
        if re.search("[a-zA-Z]{2,3}\d{4}", str(tmp)):
            if log:
                self.flag("Possible ID")
            return 1
        else:
            return 0
    def flag(self, reason="invalid"):
        self.flagged.append([self.index, self.q, self.data.loc[self.index, self.q], reason])
    def cleanNumeric(self, q, index):
        self.index = index
        self.q = q
        tmp = self.data.loc[index,q]
        if self.validID(tmp):
            return
        elif isinstance(tmp, float) or isinstance(tmp, int) or str(tmp).isnumeric():
            return
        elif tmp == ".":
            self.data.loc[index,q] = ""
        else:
            self.data.loc[index,q] = self.data.loc[index,q].replace("O", "0")
            self.data.loc[index,q] = re.sub("\D", "", self.data.loc[index,q])
        self.logChange("numeric", tmp)
    def standardizeEmployment(self, q, index, employedq="QID81 - ¿Está empleada/o actualmente?"):
        sjob = str(self.data.loc[index,q]).lower().strip()
        for job in jobs:
            if str(self.data.loc[index,q]).lower().strip() in job[1]: # keeps the thing they put in, but puts it in brackets after "no" if they said "no" to "are you employed"
                sjob = job[0]
                break
        if str(self.data.loc[index,employedq]).lower().strip() == "no":
            self.data.loc[index,q] = "no (" + str(sjob) +  ")"
        else:
            self.data.loc[index,q] = sjob
    def cleanBinary(self, q, index):
        self.index = index
        self.q = q
        tmp = str(self.data.loc[index,q])
        if self.validID(tmp):
            return
        self.data.loc[index,q] = str(self.data.loc[index,q]).lower()
        if "no" in self.data.loc[index,q] or "desemplead" in self.data.loc[index,q] or "retirada" in self.data.loc[index,q] or "voluntari" in self.data.loc[index,q]: # check next col to see what job is, if none then no
            self.data.loc[index,q] = "no"
        elif "sí" in self.data.loc[index,q] or "si" in self.data.loc[index,q] or "emplead" in self.data.loc[index,q]:
            self.data.loc[index,q] = "si"
        else:
            self.flag()
        self.logChange("binary", tmp)
    def cleanID(self, index): # fix pls
        self.index = index
        self.q =  id
        tmp = str(self.data.loc[index, id]).upper().strip(" ")
        nloc = ""
        try:
            self.data.loc[index, id] = re.search("[a-zA-Z]{2,3}\d{4}", tmp).group(0)
        except:
            self.flag()
        self.logChange("id", tmp)
    def getDupePairs(self, dupes):
         pairs, group, nans = [], [], []
         tmp = ""
         for idx, row in dupes.iterrows():
             try:
                 if math.isnan(float(row[id])) or row[id] == "NaN":
                     nans.append(row)
             except:
                if row[id] == tmp or tmp == "":
                    pass
                else:
                    pairs.append(group)
                    group = []
                tmp = row[id]
         pairs.append(group)
         return pairs, nans
    def resolveIdDupes(self):
         dupes = self.data[self.data.duplicated(subset=[id], keep=False)].sort_values(by=[id])
         pairs, nans = self.getDupePairs(dupes)
         if pairs == [[]] and nans == []:
             print("No collisions detected!")
         else:
            dupes.to_excel(self.name + "_collisions.xlsx")
            print("Collisions will be written to " + self.name + "_collisions.xlsx")
    def merge(self, other):
        try:
            self.merged = self.data.merge(other.data, left_on=[id,post], right_on=[id,post], validate="1:1")
            print("merged!")
        except Exception as e:
            print(e)
    def cleanColumn(self, dtype, colname=""):
        if dtype.lower() == "binary":
            for idx, row in self.data.iterrows():
                self.cleanBinary(colname, idx)
        elif dtype.lower() == "numeric":
            for idx, row in self.data.iterrows():
                self.cleanNumeric(colname, idx)
        elif dtype.lower() == "id":
            for idx, row in self.data.iterrows():
                self.cleanID(idx)
        elif dtype.lower() == "job":
            for idx, row in self.data.iterrows():
                self.standardizeEmployment(colname, idx)
        else:
            print("Sorry! " + dtype + " is not a valid datatype. Please enter either binary, numeric, or id")
    def write(self):
        self.data.compare(self.read).to_excel(self.name + "_diff.xlsx")
        self.data.to_excel(self.name + "_cleaned.xlsx")
        if self.merged != "":
            self.merged.to_excel(self.name + "_merged.xlsx")
        if self.flagged != "":
            pd.DataFrame(self.flagged,columns=["index", "question", "value", "reason(optional)"]).to_excel(self.name + "_flagged.xlsx")
        if self.changes != []:
            with open(self.name + "_changes.txt", "w") as f:
                for change in self.changes:
                    f.write("\n")
                    f.write(change)
