#!/usr/bin/env python3
import neoclean
s = neoclean.survey("SurveyClean.xlsx")
d = neoclean.survey("HistoryClean.xlsx")
surveyDefaultNumericQs = ["Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?", "QID80 - ¿Cuántas personas viven con Usted?"]
surveyDefaultBinaryQs = ["QID81 - ¿Está empleada/o actualmente?", "¿Sabe Usted lo que son las pruebas genéticas?", "¿Te has hecho una prueba genética alguna vez?", "Exámen de seno / Mamografía", "Exámen cervical / Papanicolao", "Exámen colorectal / Colonoscopía"]
historyDefaultNumericQs = ["Por favor complete con sus datos: - Edad"]
for i in range(len(surveyDefaultNumericQs)):
    s.cleanColumn("numeric", surveyDefaultNumericQs[i])
for i in range(len(surveyDefaultBinaryQs)):
    s.cleanColumn("binary", surveyDefaultBinaryQs[i])
d.cleanColumn("numeric", historyDefaultNumericQs[0])
s.cleanColumn("id")
d.cleanColumn("id")
s.cleanColumn("job", "QID82 - ¿Cuál es su trabajo?")
s.resolveIdDupes()
d.resolveIdDupes()
s.write()
s.merge(d)
