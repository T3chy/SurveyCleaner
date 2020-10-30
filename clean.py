import pandas as pd
import re
import math
survey = pd.read_excel("SurveyClean.xlsx")
purleynumeric = ["Por favor complete con sus datos: - Código Postal","Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?"]
yearranges = ["Por favor complete con sus datos: - Código Postal","Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela primaria (hasta qué año) - Texto", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela media (hasta qué año) - Texto", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela secundaria/preparatoria (hasta qué año) - Texto"]
def toPureNumeric(value): # no return cuz pass by reference, baby
    if isinstance(value, str):
        value = value.replace("O", "0")
        value = value.replace("o","0")
        re.sub("\D", "", value)
    else:
        pass
    return value
for index, response in survey.iterrows():
    for q in purleynumeric: # remove letters from purley numeric fields, hopefully catching O (oh) vs 0 (zero) and similar
        tmp = response[q]
        response[q] = toPureNumeric(response[q])
        #print(response[q])
        if response[q] != tmp and not (isinstance(response[q], float) and  math.isnan(response[q])):
            print("GOT ONE! Replaced " + tmp + " with " + response[q])
    for q in purleynumeric[1:]: # removes accidental ID and similar b/c no age or range of years would be > 100 in human context
        tmp = response[q]
        if not (isinstance(response[q], float) and  math.isnan(response[q])):
            print(tmp)
            tmp = toPureNumeric(tmp)
            if tmp == "."  or int(tmp) > 100:
                print("GOT ONE! Deleting %s because it is nonsensical here", response[q])
                response[q] = ""
        

