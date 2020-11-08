import neoclean
all = 0
d = neoclean.survey("HistoryClean.xlsx")
s = neoclean.survey("SurveyClean.xlsx")
if all:
    s.cleanNumeric(["Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?"])
    s.write()
    s.removeDirectDupes()
    s.resolveIdDupes()
    s.merge(d)
    s.cleanID()
else:
    s.resolveIdDupes()
    s.resolveIdDupes()
    d.resolveIdDupes()
    d.resolveIdDupes()
    s.merge(d)
