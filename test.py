#!/usr/bin/env python3
import neoclean
s = neoclean.survey("SurveyClean.xlsx")
surveyDefaultNumericQs = ["Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?", "QID80 - ¿Cuántas personas viven con Usted?"]
surveyDefaultBinaryQs = ["QID81 - ¿Está empleada/o actualmente?", "¿Sabe Usted lo que son las pruebas genéticas?", "¿Te has hecho una prueba genética alguna vez?", "Exámen de seno / Mamografía", "Exámen cervical / Papanicolao", "Exámen colorectal / Colonoscopía"]
for i in range(len(surveyDefaultNumericQs)):
    s.cleanColumn("numeric", surveyDefaultNumericQs[i])
for i in range(len(surveyDefaultBinaryQs)):
    s.cleanColumn("binary", surveyDefaultBinaryQs[i])
s.cleanColumn("id")
s.cleanColumn("job", "QID82 - ¿Cuál es su trabajo?")
s.resolveIdDupes()
s.write()
