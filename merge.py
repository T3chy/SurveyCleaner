import pandas as pd
def merge(survey, history):
    survey = pd.read_excel(survey)
    history = pd.read_excel(history)
    try:
        merged = survey.merge(history, left_on= "Por favor complete con sus datos: - Número de identificación del estudio", right_on="Unnamed: 17")#, validate="1:1")
    except:
        print("collisions!")
        merged = pd.DataFrame()
    return merged
merge("SurveyClean_cleaned.xlsx","HistoryClean.xlsx").to_excel("merged.xlsx")
