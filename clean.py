
# multiple choice less short answer?
import pandas as pd
import re
import math
changes = []
id = "Por favor complete con sus datos: - Número de identificación del estudio"
post = "Por favor complete con sus datos: - Código Postal"
tobecleaned = "SurveyClean.xlsx"
read = pd.read_excel(tobecleaned)
survey = read.copy()
isSurvey = 1
if isSurvey:
    purleynumeric = [post,"Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?"]
    yearranges = [post,"Por favor complete con sus datos: - Edad", "QID73 - ¿Hace cuántos años vive en los Estados Unidos?","QID80 - ¿Cuántas personas viven con Usted?", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela primaria (hasta qué año) - Texto", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela media (hasta qué año) - Texto", "¿Cuál es el nivel más alto de educación que ha completado? - Escuela secundaria/preparatoria (hasta qué año) - Texto"]
    binaryranges = ["QID81 - ¿Está empleada/o actualmente?","¿Sabe Usted lo que son las pruebas genéticas?","¿Te has hecho una prueba genética alguna vez?", "Exámen de seno / Mamografía", "Exámen cervical / Papanicolao", "Exámen colorectal / Colonoscopía"]
else:
    purleynumeric = [post, "Por favor complete con sus datos: - Edad"]
sfzipcodes = [94016,94112,94017,94127,94132,94014,94015,94005,94131,94134,94116,94114,94110,94080,94122,94117,94124,94083,94119,94120,94125,94126,94137,94139,94140,94141,94142,94143,94144,94145,94146,94147,94151,94159,94160,94161,94163,94164,94172,94177,94188,94118,94103,94102,94121,94107,94115,94158,94066,94129,94108,94109,94044,94104,94105,94123,94111,94128,94133,94030,94130,94011,94965,94966,94010,94501,94607,94037,94502,94038,94401,94604,94614,94620,94622,94623,94624,94649,94659,94660,94661,94666,94617,94497,94920,94612,94608,94615,94662,94606,94402,94621,94609,94610,94710,94941,94601,94018,94403,94702,94942,94404,94703,94925,94701,94712,94618,94602,94706,94807,94976,94603,94611,94705,94709,94613,94720,94002,94974,94977,94804,94577,94964,94704,94939,94019,94707,94579,94065,94619,94605,94802,94808,94850,94516,94708,94904,94530,94580,94801,94070,94578,94805,94563,94970,94901,94957] # all zipcodes within 40km of 94016
saczipcodes = [94203,94204,94205,94206,94207,94208,94209,94211,94229,94230,94232,94234,94235,94236,94237,94239,94240,94244,94245,94247,94248,94249,94250,94252,94254,94256,94257,94258,94259,94261,94262,94263,94267,94268,94269,94271,94273,94274,94277,94278,94279,94280,94282,94283,94284,94285,94287,94288,94289,94290,94291,94293,94294,94295,94296,94297,94298,94299,95840,95851,95852,95853,95860,95865,95866,95867,95894,95899,95812,95813,95814,95811,95816,95818,95798,95799,95833,95605,95815,95817,95819,95820,95834,95822,95825,95838,95824,95691,95864,95835,95826,95831,95821,95652,95673,95823,95828,95660,95618,95832,95609,95827,95608,95841,95836,95837,95741,95842,95829,95758,95626,95655,95843,95670,95776,95621,95612,95830,95617,95759,95628,95624,95610,95611,95639,95747,95742,95662,95661,95757,95678,95616,95668,95693,95763] # all zipcodes within 30km of 94203
lazipcodes = [90001,90003,90002,90255,90011,90058,90044,90037,90270,90059,90047,90021,90061,90089,90023,90280,90062,90007,90222,90262,90201,90015,90014,90305,90013,90043,90030,90050,90051,90052,90053,90054,90055,90060,90072,90074,90075,90076,90078,90080,90081,90082,90083,90086,90087,90088,90093,90009,90018,90303,90071,90079,90202,90017,90223,90224,90040,90033,90006,90091,90189,90099,90063,90070,90311,90306,90307,90308,90309,90310,90312,90008,90302,90247,90057,90012,90249,90301,90248,90022,90220,90090,90005,90221,90723,90250,90304,90239,90251,90026,90242,90010,90020,90016,90019,90056,90241,90096,90031,90240,90747,90746,90506,91754,90004,90640,90029,90504,90032,90260,90805,90661,90662,90230,90036,90232,90045,90706,90231,90233,90261,90038,91803,90660,90895,91755,91756,90034,90671,90035,90065,90094,90245,90028,90707,90278,90211,90048,90502,90749,90039,90042,91804,90745,90610,91801,90266,90606,90267,90711,90714,90501,90712,90212,90807,90066,90651,90652,90810,91716,90650,91714,91715,90507,90508,90509,90510,91802,91896,91899,90027,90295,91030,90503,91204,90209,90213,91205,90067,90064,90293,90069,90292,91770,91031,90041,90254,90296,90670,90046,90713,91209,91221,91222,91224,91225,91226,91778,91210,91776,90068,90806,90702,90701,90294,91733,90025,90607,90608,90609,90024,91203,90291,90710,90602,91771,91772,90755,90703,91105,90277,91108,90808,91123,91608,90601,90405,90084,90095,90073,91522,90505,91393,90210,91106,90717,91775,90404,90715,90748,91521,91523,91206,91102,91109,91110,91114,91115,91116,91117,91118,91121,91124,91125,91126,91129,91182,91184,91185,91188,91189,90605,90744,91101,91202,91731,90813,91201,91602,90604,90716,91604,90637,90639,91103,90804,90831,90406,90407,90408,90409,90410,90411,90833,91734,91735,91506,90401,91780,90403,90623,91502,90815,90603,90638,90801,90809,90832,90842,90844,90846,90847,90848,90853,90077,91503,91507,91508,91510,91526,91207,91732,91601,90402,91208,91505,90814,91746,90840,91745,91104,91199,91007,90721,90274,91603,91609,91610,91611,91612,91614,91615,91616,91617,91618,90802,90049,91607,91107,91423,91501,90731,90621,90622,90624,90732,90630,90720,91021,90275,90803,90822,91003,91046,91012,91504,91020,90620,91006,90733,90734,91001,91066,91077,91413,91606,90631,91025,91495,91403,91747,91749,92833,90632,90633,91401,91024,91214,90740,91706,91605,91353,92845,91744,90272,91352,91411,91404,91407,91408,91409,91410,91470,91482,91496,91499,91017,91790,92801,90680,91793,91436,92804,92809,91009,91416,91426,90743,91043,91405,91334,91011,91748,92832,92841,91016,91316,92835,91008,92684,91010,91023,90742,91792,91041,92649,92822,91406,91412,91402,92821,92834,92836,92837,92838,91356,91042,91722,92683,92899,92831,92803,92812,92814,92815,92816,92817,92825,92850,92685,91791,92844,91331,92805,91040,92655,92647,91723,92802,92842,92846,91788,90290,91357,91702,92840,91333,91343,91789,90264,91337,91385,91335,92871,91346,91395,92870,92605,91364,91325,91345,91724,91371,91341,92806,92843,91327,91328,91329,91340,92648,91365,91330,92868,91765,91396,92865,92703,91306,92728,91740,92708,92811,91367,91324,92706,91305,91308,91309,91303,91394,91372,92823,91392,91302,92615,92704,92856,92857,92859,92863,92864,91342,92885,91741,91344,92866,90263,91773,91768,92646,92702,92711,92712,92799,92867,92886,92735,92861,92701,91326,92807,91313,91304,91766,92626,92707,91769,92869,92627,91311,91321,92780,92705,92781,91307,93563,92628,91709,92663,92887,91767,92782,92808,92658,92659,91750,92606,92614,91376,92660,90265,91301,91763,92698,92616,92619,92623,91711,91382,93064,92661,92697,91387,92612,92617,91322,92602,92604,92662,91386,91377,91710,92862,93063,92620,92625,91351,93510,91708,91350,91381,91786,91758,92650,93099,91762,91785,92603,91380,93094,92657,92618,91784,91362,91358,91359,91383,92880,93550,91355,93062,91354,93065,92882,92610,91761,91361,91743,91764,91729,92637,93553,92860,91730,91701,92877,92878,92630,92676,91360,91390,92607,92652,92654,92651,91310,91737,93543,92653,92609,91319,92656,91752,92879,93021,90704,93551,92691,92690,93020,93590,93599,93552,91739,92692,91320,92505,93040,92678,92677,92688,91759,91384,93544,93012,92337,92694,92358,92881,92335,93015,92883,92509,92629,92397,92679,92503] # all zipcodes within 75km of 90001
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
            value = ""
    else:
        value = value
    return value
def resolveDupes(survey):
    survey.drop_duplicates()
    survey = survey[survey.duplicated(subset=[id])]
    return survey
def inferLoc(zipcode):
    if zipcode in lazipdoes:
        return "LA"
    if zipcode in saczipcodes:
        return "SAC"
    if zipcode in sfzipcodes:
        return "SF"
def handleID(value,zipcode):
 #   try:
    if isinstance(value,str):
        value = value.strip(" ")
        print(value + "b")
        if value == re.search("[A-Z]{3}\d{4}", value).group(0) or value == re.search("[A-Z]{2}\d{4}", value).group(0):
            return value
        elif value == re.search("\d{4}", value).group(0):
            return value + inferLoc(zipcode)
        else:
            return ""
  #  except:
   #     return "-1"
for index, response in survey.iterrows():
    for q in purleynumeric: # remove letters from purley numeric fields, hopefully .locching O (oh) vs 0 (zero) and similar
        tmp = response[q]
        response[q] = toPureNumeric(response[q])
        #print(response[q])
        if response[q] != tmp and not (isinstance(response[q], float) and  math.isnan(response[q])):
            print("GOT ONE! Replaced " + tmp + " with " + str(response[q]) +  " at respondant " + str(response[id]) + " question: " + q)
            changes.append("NUMERIC RESPONSE: Replaced " + str(tmp) + " with " + str(response[q]) + ". respondant " + str(response[id]) + " question: "  + q)
        survey.loc[index,q] = response[q]
    for q in yearranges[1:]: # removes accidental ID and similar b/c no age or range of years would be > 100 in human context
        tmp = response[q]
        if not (isinstance(response[q], float) and  math.isnan(response[q])):
            tmp = toPureNumeric(tmp)
            if tmp == "":
                pass
            elif tmp == "."  or int(tmp) > 100:
                print("GOT ONE! Deleting " + str(response[q]) +  " at respondant " + str(response[id]) + " question: " + q +" because it is nonsensical here")
                changes.append("NUMERIC RESPONSE: Deleted " + str(response[q]) +  " respondant " + str(response[id]) + " question: " + q +" because it is nonsensical here")
                response[q] = ""
            survey.loc[index,q] = response[q]
    for q in binaryranges: # normalize yes/no questions
        tmp = response[q]
        response[q] = handleBinary(response[q])
        if response[q] != str(tmp).lower():
            print("GOT ONE! replaced " + str(tmp) + " with " + str(response[q]));
            changes.append("BINARY RESPONSE: Replaced " + str(tmp) + " with " + str(response[q]) + " respondant " + str(response[id]) + " question: "  + q )
        survey.loc[index,q] = str(response[q]).lower()
    tmp = response[id]
    response[id] = handleID(response[id],response[post])
    if tmp != response[id]:
        print("GOT ONE! replaced " + str(tmp) + " with " + str(response[id]))
        changes.append("ID: Replaced " + str(tmp) + " with " +  str(response[id]))
    survey.loc[index,id] = str(response[id])
#survey.to_excel(tobecleaned.strip(".xlsx") + "_cleaned.xlsx")
survey.compare(read).to_excel("diff.xlsx")
survey = resolveDupes(survey)
survey.to_excel("clean.xlsx")
file = open(str(tobecleaned.strip(".xlsx") + "_changes.txt"), "w")
print("cleaned excel written to " + (tobecleaned.strip(".xlsx") + "_cleaned.xlsx"))
print("spreadsheet of differences written to diff.xlsx")
print("cleaned excel written to " + str(tobecleaned.strip(".xlsx") + "_changes.txt"))
for change in changes:
    file.writelines(change)
    file.writelines("\n")
file.close()
