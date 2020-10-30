import pandas as pd
import re
import math
changes = []
tobecleaned = "SurveyClean.xlsx"
survey = pd.read_excel(tobecleaned)
purleynumeric = ["Por favor complete con sus datos: - Código Postal","Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?"]
yearranges = ["Por favor complete con sus datos: - Código Postal","Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela primaria (hasta qué año) - Texto", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela media (hasta qué año) - Texto", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela secundaria/preparatoria (hasta qué año) - Texto"]
binaryranges = ["QID81 - ¿Está empleada/o actualmente?","¿Sabe Usted lo que son las pruebas genéticas?","¿Te has hecho una prueba genética alguna vez?", "Exámen de seno / Mamografía", "Exámen cervical / Papanicolao", "Exámen colorectal / Colonoscopía"]
def toPureNumeric(value): # no return cuz pass by reference, baby
    if isinstance(value, str):
        value = value.replace("O", "0")
        value = re.sub("\D", "", value)
    else:
        pass
    return value
def handleBinary(value):
    if isinstance(value, str):
        value = value.lower()
        if not (value == "no" or value== "si" or value == "sí"):
            value = "no"
        value = value.replace("i", "í")
        if value == ".":
            value = "no"
    else:
        value = "no"
    return value
for index, response in survey.iterrows():
    for q in purleynumeric: # remove letters from purley numeric fields, hopefully catching O (oh) vs 0 (zero) and similar
        tmp = response[q]
        response[q] = toPureNumeric(response[q])
        #print(response[q])
        if response[q] != tmp and not (isinstance(response[q], float) and  math.isnan(response[q])):
            print("GOT ONE! Replaced " + tmp + " with " + response[q]+  " at respondant " + str(response["Por favor complete con sus datos: - Número de identificación del estudio"]) + " question: " + q)
            changes.append("NUMERIC RESPONSE: Replaced " + str(tmp) + " with " + str(response[q]) + " at respondant " + str(response["Por favor complete con sus datos: - Número de identificación del estudio"]) + " question: "  + q)
            survey.loc[index][q] = response[q]
    for q in purleynumeric[1:]: # removes accidental ID and similar b/c no age or range of years would be > 100 in human context
        tmp = response[q]
        if not (isinstance(response[q], float) and  math.isnan(response[q])):
            tmp = toPureNumeric(tmp)
            if tmp == "":
                pass
            elif tmp == "."  or int(tmp) > 100:
                print("GOT ONE! Deleting " + response[q] +  " at respondant " + str(index) + " question: " + q +" because it is nonsensical here")
                changes.append("NUMERIC RESPONSE: Deleted " + response[q] +  " at respondant " + str(response["Por favor complete con sus datos: - Número de identificación del estudio"]) + " question: " + q +" because it is nonsensical here")
                response[q] = ""
                survey.loc[index][q] = response[q]
    for q in binaryranges: # normalize yes/no questions 
        tmp = response[q]
        response[q] = handleBinary(response[q])
        if response[q] != str(tmp).lower():
            print("GOT ONE! replaced " + str(tmp) + " with " + str(response[q]));
            changes.append("BINARY RESPONSE: Replaced " + str(tmp) + " with " + str(response[q]) + " at respondant " + str(response["Por favor complete con sus datos: - Número de identificación del estudio"]) + " question: "  + q )
            survey.loc[index][q] = response[q]
file = open(str(tobecleaned.strip(".xlsx") + "_changes.txt"), "w")
survey.to_excel(tobecleaned.strip(".xlsx") + "_cleaned.xlsx")
for change in changes:
    file.writelines(change)
    file.writelines("\n")
file.close()