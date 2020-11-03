import pandas as pd
import re
import math
id = "Por favor complete con sus datos: - Número de identificación del estudio"
class survey:
    def __init__(self,name):
        self.name = name.strip("xlsx")
        self.read = pd.read_excel(name)
        self.data = self.read.copy()
        self.changes = []
        self.flagged = []
    def possibleID(tmp):
        try:
            if tmp == re.search("[A-Z]{3}\d{4}", tmp).group(0) or tmp == re.search("[A-Z]{2}\d{4}", tmp).group(0):
                self.flagged.append("POSSIBLE ID FOUND: " + str(tmp) + " at respondant # " + str(index) + " question " + str(q))
                return 1
        except:
            return 0
    def cleanNumeric(self, qs):
        for index, respondant in self.data.iterrows():
            for q in qs:
                tmp = self.data[index,q]
                if isinstance(tmp, float) or isinstance(tmp, int) or str(tmp).isnumeric():
                    pass
                elif tmp == ".":
                    self.data[index,q] = ""
                    self.changes.append("NUMERIC: Replaced . with an empty string at respondant" + str(self.data[index,id]) + " question " + str(q))
                else:
                    if possibleID(tmp):
                        pass
                    else:
                        self.data[index,q] = self.data[index,q].replace("O", "0")
                        self.data[index,q] = self.data[index,q].sub("\D", "", self.data[index,q])
                        self.changes.append("NUMERIC: Replaced " + tmp + " with " +  str(self.data[index,q]) + " at respondant " + str(self.data[index,id]) + " question " +  str(q))
    def cleanBinary(self, qs):
        for index, respondant in self.data.iterrows():
            for q in qs:
                tmp = str(self.data[index,q])
                self.data[index,q] = self.data[index,q].lower()
                if "no" in self.data[index,q]:
                    self.data[index,q] = "no"
                if "sí" in self.data[index,q] or "si" in self.data[index,q]:
                    self.data[index,q] = "si"
                else:
                    self.flagged.append(["respondant " + str(index), "question " + str(q), self.data[index,q]])
                if str(self.data[index,q]).lower() != tmp.lower():
                    self.changes.append("BINARY: Replaced " +  tmp + " with " + str(self.data[index,q] + " at respondant" + str(self.data[index,id]) + " question " + str(q)))
    def write(self):
        self.data.compare(self.read).to_excel(self.name + "_diff.xlsx")
        self.data.to_excel(self.name + "_cleaned.xlsx")
        self.flagged.to_excel(self.name + "_flagged.xlsx")
        with open(self.name + "_changes.txt", "w") as f:
            for change in changes:
                f.write(change)
                f.write("\n")
