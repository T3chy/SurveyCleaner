import pandas as pd
def merge(survey, history):
    read = pd.read_excel(survey)
    survey = read.copy()
    read = pd.read_excel(history, skiprows=1).copy()
    history = read.copy()
    survey[["Por favor complete con sus datos: - Número de identificación del estudio"]] = survey["Por favor complete con sus datos: - Número de identificación del estudio"].astype('U')
    history[["Por favor complete con sus datos: - Número de identificación del estudio"]] = history["Por favor complete con sus datos: - Número de identificación del estudio"].astype('U')
    print(survey["Por favor complete con sus datos: - Número de identificación del estudio"])
    print(history["Por favor complete con sus datos: - Número de identificación del estudio"])
    #try:
    #    merged = survey.merge(history, left_on="Por favor complete con sus datos: - Número de identificación del estudio", right_on="Por favor complete con sus datos: - Número de identificación del estudio")#, validate="1:1")
    #except Exception as e:
    print("collisions!")
    print("Survey collisions: " + survey.duplicated(subset=["Por favor complete con sus datos: - Número de identificación del estudio"]))
    print("History collisions: " + history.duplicated(subset=["Por favor complete con sus datos: - Número de identificación del estudio"]))
    merged = pd.DataFrame()
    return merged
merge("SurveyClean_cleaned.xlsx","HistoryClean.xlsx").to_excel("merged.xlsx")
