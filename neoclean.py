import numpy as np
import pandas as pd
import re
import math
id = "Por favor complete con sus datos: - Número de identificación del estudio"
post = "Por favor complete con sus datos: - Código Postal"
pd.options.display.max_rows = 999
class survey:
    def __init__(self,name):
        self.name = name.strip(".xlsx")
        self.read = pd.read_excel(name)
        self.data = self.read.copy()
        self.changes = []
        self.flagged = []
        self.index = 0
        self.q = ""
    def possibleID(self,tmp, log=True):
       # if re.search("[A-Z]{2}\d{4}", tmp) or re.search("[A-Z]{3}\d{4}", tmp):
        if re.search("[A-Z].*?\d{4}", str(tmp)):
            if log:
                self.flagged.append(["POSSIBLE ID FOUND: " + str(tmp), "respondant # " + str(self.index), str(self.q)])
            return 1
        else:
            return 0
    def cleanNumeric(self, qs,):
        for index, respondant in self.data.iterrows():
            self.index = index
            for q in qs:
                self.q = q
                tmp = self.data.loc[index,q]
                if self.possibleID(tmp):
                    pass
                elif isinstance(tmp, float) or isinstance(tmp, int) or str(tmp).isnumeric():
                    pass
                elif tmp == ".":
                    self.data.loc[index,q] = ""
                    self.changes.append("NUMERIC: Replaced . with an empty string at respondant" + str(self.data.loc[index,id]) + " question " + str(q))
                else:
                    self.data.loc[index,q] = self.data.loc[index,q].replace("O", "0")
                    self.data.loc[index,q] = re.sub("\D", "", self.data.loc[index,q])
                    self.changes.append("NUMERIC: Replaced " + tmp + " with " +  str(self.data.loc[index,q]) + " at respondant " + str(self.data.loc[index,id]) + " question " +  str(q)) # maybe don't log just lowercasing
    def cleanBinary(self, qs):
        for index, respondant in self.data.iterrows():
            self.index = index
            for q in qs:
                self.q = q
                tmp = str(self.data.loc[index,q])
                if self.possibleID(tmp):
                    continue
                self.data.loc[index,q] = str(self.data.loc[index,q]).lower()
                if "no" in self.data.loc[index,q] or "desemplead" in self.data.loc[index,q]: # ask Laura abt this one or "voluntaria" in self.data.loc[index,q]:
                    self.data.loc[index,q] = "no"
                elif "sí" in self.data.loc[index,q] or "si" in self.data.loc[index,q] or "emplead" in self.data.loc[index,q]:
                    self.data.loc[index,q] = "si"
                elif "voluntari" in self.data.loc[index,q]:
                    self.data.loc[index,q]= "voluntaria"
                else:
                    self.flagged.append([ str(index), str(q), self.data.loc[index,q]])
                if str(self.data.loc[index,q]).lower() != tmp.lower():
                    self.changes.append("BINARY: Replaced " +  tmp + " with " + str(self.data.loc[index,q] + " at respondant" + str(self.data.loc[index,id]) + " question " + str(q)))
    def inferLoc(self,value):
        if self.possibleID(value):
            return 1
        if re.search("\d{4}",str(value)):
            if self.data[self.idx,post] in SAC:
               return "SAC" + value
            elif self.data[self.idx,post] in LA:
               return "LA" + value
            elif self.data[self.idx,post] in SF:
               return "SF" + value
        return 0
    def cleanID(self):
        self.q = id
        for index, respondant in self.data.iterrows():
            self.index = index
            tmp = self.data.loc[index, id].upper()
            nloc = self.inferLoc(respondant[id])
            if self.possibleID(respondant[id], log=False) and nloc:
                if nloc != tmp and nloc != 1:
                    self.changes.append("ID: Replaced " + tmp + " with " +  nloc + " by infering location with zipcode " + respondant[post])
                    self.data.loc[index,id] = nloc if nloc != 1 else tmp
                else:
                    self.data.loc[index, id] = ""
                    self.changes.append("ID: Deleted " + tmp  + " because it is not a valid ID")
    def removeDirectDupes(self):
        tmp= self.data
        self.data = self.data.drop_duplicates()
        if not self.data.equals(tmp):
            pass
        else:
            print("no direct duplicates!")
    def getDupePairs(self, dupes):
         pairs= []
         group = []
         nans = []
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
                group.append(row)
                tmp = row[id]
         pairs.append(group)
         return pairs, nans
    def resolveIdDupes(self, other=None):
         dupes = self.data[self.data.duplicated(subset=[id], keep=False)].sort_values(by=[id])
         print(dupes[id])
         try:
             otherdupes = other[other.duplicated(subset=[id], keep=False)]
             otherdupes = otherdupes.groupby(by=[id])
         except:
             otherdupes = -1
         pairs, nans = self.getDupePairs(dupes)
         if pairs == [[]] and nans == []:
             print("No collisions detected!")
         else:
             choice = input(str(len(pairs)) + " duplicate pair(s) detected! Would you like to resolve them here? [y/N]\n")
             if choice.lower() == "y" or choice.lower() == "yes":
                 if pairs != [[]]:
                     for pair in pairs:
                         print("____________________________________________________________________________________")
                         print("Colliding id detected!")
                         n = 1
                         for bruh in pair:
                             print("____________________________________________________________________________________")
                             print("Respondant " + str(n) + ":")
                             print(bruh)
                             n += 1
                         choice = "N"
                         while not isinstance(choice, int):
                            try:
                                choice = int(input("Which respondant would you like to keep?\n"))
                                if choice > len(pair):
                                    print("Please input a valid respondant number!")
                                    choice = "N"
                            except:
                                print("please input a number!")
                         n = 1
                         for bruh in pair:
                             if n == choice:
                                 pass
                             else:
                                 self.data = self.data.drop(self.data[self.data["Response ID"] == bruh["Response ID"]].index)
                             n += 1
                 if not nans == []:
                     self.handlenanID(nans)
             else:
                print("ok! Please resolve them in the original input xlsx, and rerun this script!")
    def handlenanID(self, nans):
         print("____________________________________________________________________________________")
         print(str(len(nans)) + " nan ids detected!")
         n = 1
         for bruh in nans:
             print("Respondant " + str(n) + ":")
             print(bruh[id])
             n += 1
         choice = "N"
         while not isinstance(choice, int):
            try:
                choice = int(input("Which respondant would you like to keep?\n"))
                if choice > len(nans):
                    print("Please input a valid respondant number!")
                    choice = "N"
            except:
                print("please input a number!")
         n = 1
         for bruh in nans:
             if n == choice:
                 pass
             else:
                 self.data = self.data.drop(self.data[self.data["Response ID"] == bruh["Response ID"]].index)
             n += 1
    def merge(self, other):
        try:
            self.data.merge(other.data, left_on=[id,post], right_on=[id,post], validate="1:1")
            print("merged!")
        except:
            print("Merge failed! Attempting to resolve collisions...")
            self.attemptResolvebyMerge(other)
    def attemptResolvebyMerge(self, other):
        self.resolveIdDupes(other=other.data)
        other.resolveIdDupes(other=self.data)
        try:
            self.data.merge(other.data, left_on=[id], right_on=[id], validate="1:1")
        except:
            print("fail")
    def write(self):
        self.data.compare(self.read).to_excel(self.name + "_diff.xlsx")
        self.data.to_excel(self.name + "_cleaned.xlsx")
        pd.DataFrame(self.flagged,columns=["Respondant", "question", "value"]).to_excel(self.name + "_flagged.xlsx")
        with open(self.name + "_changes.txt", "w") as f:
            for change in self.changes:
                f.write(change)
                f.write("\n")
