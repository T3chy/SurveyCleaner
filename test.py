import neoclean
d = neoclean.survey("HistoryClean.xlsx")
s = neoclean.survey("SurveyClean.xlsx")
s.cleanNumeric(["Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?"])
s.write()
s.removeDirectDupes()
s.resolveIdDupes()
s.merge(d)
s.cleanID()
