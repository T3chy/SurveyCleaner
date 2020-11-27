#!/usr/bin/env python3
import neoclean
# d = neoclean.survey("HistoryClean.xlsx")
s = neoclean.survey("SurveyClean.xlsx")
#surveyDefaultNumericQs = ["Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?", "QID80 - ¿Cuántas personas viven con Usted?"]
#surveyDefaultBinaryQs = ["QID81 - ¿Está empleada/o actualmente?", "¿Sabe Usted lo que son las pruebas genéticas?", "¿Te has hecho una prueba genética alguna vez?", "Exámen de seno / Mamografía", "Exámen cervical / Papanicolao", "Exámen colorectal / Colonoscopía"]
#for i in range(3):
#    s.cleanColumn("numeric", surveyDefaultNumericQs[i])
#    s.cleanColumn("binary", surveyDefaultBinaryQs[i])
##s.cleanColumn("id")
s.cleanColumn("job", "QID82 - ¿Cuál es su trabajo?")
s.write()
