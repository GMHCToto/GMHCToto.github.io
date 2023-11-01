import math
import os
import pandas as pd
import hockeyweerelt
import json

hw = hockeyweerelt.Api()

standings = hw.get_standing("N11")
playerdata = json.load(open("playerdata.json", "r"))
topGoals = ""
goalsAmount = -1
topAssist = ""
assistsAmount = -1
topCards = ""
cardsAmount = -1
topMotm = ""
motmAmount = -1

cleanSheets = 1

for i in playerdata:
    if i["data"]["goals"] > goalsAmount:
        goalsAmount = i["data"]["goals"]
        topGoals = [i["name"]]
    elif i["data"]["goals"] == goalsAmount:
        topGoals.append(i["name"])

    if i["data"]["assists"] > assistsAmount:
        assistsAmount = i["data"]["assists"]
        topAssist = [i["name"]]
    elif i["data"]["assists"] == assistsAmount:
        topAssist.append(i["name"])

    if i["data"]["kaarten"] > cardsAmount:
        cardsAmount = i["data"]["kaarten"]
        topCards = [i["name"]]
    elif i["data"]["kaarten"] == cardsAmount:
        topCards.append(i["name"])

    if i["data"]["motm"] > motmAmount:
        motmAmount = i["data"]["motm"]
        topMotm = [i["name"]]
    elif i["data"]["motm"] == motmAmount:
        topMotm.append(i["name"])

results = hw.get_results("N3706","N11")

#results.append({"home_team": {"club_name": "Goudse MHC"}, "away_team":{"club_name":"K.H.C. Strawberries"},"home_score":0,"away_score":0})
matches = [["Goudse MHC", "K.H.C. Strawberries"],
["Dopie", "Goudse MHC"],
["Hockey Club Wateringse Veld", "Goudse MHC"],
["Goudse MHC", "HMHC Saxenburg"],
["HCC Catwyck", "Goudse MHC"],
["Goudse MHC", "Z.H.C. de Kraaien"],
["MHC Voorhout", "Goudse MHC"],
["Goudse MHC", "HC Nieuwkoop"],
["HV Westland", "Goudse MHC"],
["Goudse MHC", "H.C. Haarlem"],
["Scoop Delft", "Goudse MHC"],
]
match_index = 0
wedstrijden_parsed = []
for i in results[::-1]:
    if match_index > len(matches):
        break
    if i["home_team"]["club_name"] == matches[match_index][0] and i["away_team"]["club_name"] == matches[match_index][1]:
        wedstrijden_parsed.append({"Thuis": i["home_score"],"Uit": i["away_score"]})
        match_index += 1


ranking = []

path = "voorspellingen/"
names = []
for filename in os.listdir(path):
    output_html = f'voorspellingen/{filename}'
    name = os.path.splitext(filename)[0]

    table_MN = pd.read_html(output_html)
    with open(output_html, "w") as f:
        f.write(f"<h1>{name}</h1></br>")

    total_points = 0

    df = table_MN[0]
    for i, row in df.iterrows():
        if i < len(wedstrijden_parsed): # match played
            punten = 0
            homeCorrect = wedstrijden_parsed[i]["Thuis"]
            awayCorrect = wedstrijden_parsed[i]["Uit"]
            homeGuess = df.at[i, "Thuis score"]
            awayGuess = df.at[i, "Uit score"]

            if homeGuess > awayGuess and homeCorrect > awayCorrect:
                punten = 2
                total_points += 2
            elif homeGuess == awayGuess and homeCorrect == awayCorrect:
                punten = 2
                total_points += 2
            elif homeGuess < awayGuess and homeCorrect < awayCorrect:
                punten = 2
                total_points += 2
            if homeGuess == homeCorrect:
                punten += 2
                total_points += 2
            if  awayGuess == awayCorrect:
                punten += 2
                total_points += 2
            
            df.at[i, "Score Thuis Geworden"] = homeCorrect
            df.at[i, "Score Uit Geworden"] = awayCorrect
            df.at[i, "Punten"] = punten
            
        else: # match not played
            df.at[i, "Score Thuis Geworden"] = "Nvt"
            df.at[i, "Score Uit Geworden"] = "Nvt"
            df.at[i, "Punten"] = "Nvt"

    print(df)
    with open(output_html, 'a') as f:
            f.write(df.to_html(index=False))
            f.write("</br>")

    df = table_MN[1]

    for i, row in df.iterrows():
        club_name = standings[0]["standings"][i]["team"]["club_name"]
        df.at[i,'Ranglijst'] = club_name
        if club_name == "Goudse MHC":
            gmhc_rank = standings[0]["standings"][i]["rank"]

        if df.at[i,'Ranglijst'] == df.at[i, "team"]:
            df.at[i,'Punten'] = 2
            total_points+=2
        else:
            df.at[i,'Punten'] = 0
    print(df)
    with open(output_html, 'a') as f:
            f.write(df.to_html(index=False))
            f.write("</br>")

        
    df = table_MN[2]


    if gmhc_rank <= 2:
        watGaatHeren1Doen = "Promoveren"
    elif gmhc_rank >= 11:
        watGaatHeren1Doen = "Degraderen"
    else:
        watGaatHeren1Doen = "Handhaven"

    df.at[0,"Correct"] = watGaatHeren1Doen
    df.at[1,"Correct"] = ", ".join(topGoals)
    df.at[2,"Correct"] = goalsAmount
    df.at[3,"Correct"] = ", ".join(topAssist)
    df.at[4,"Correct"] = assistsAmount
    df.at[5,"Correct"] = ", ".join(topMotm)
    df.at[6,"Correct"] = ", ".join(topCards)
    df.at[7,"Correct"] = cleanSheets
    for i in range(8):
        df.at[i, "Punten"] = 0
    if watGaatHeren1Doen == df.at[0,"Antwoord"]:
        df.at[0,"Punten"] = 5
        total_points += 5
    if df.at[1,"Antwoord"] in topGoals:
        df.at[1,"Punten"] = 5
        total_points += 5
    diff = abs(goalsAmount - int(df.at[2, "Antwoord"]))
    if diff < 10:
        df.at[2, "Punten"] = 10 - diff
        total_points += 10 - diff
    if df.at[3,"Antwoord"] in topAssist:
        df.at[3,"Punten"] = 5
        total_points += 5
    diff = abs(assistsAmount - int(df.at[4, "Antwoord"]))
    if diff < 10:
        df.at[4, "Punten"] = 10 - diff
        total_points += 10 - diff
    if df.at[5, "Antwoord"] in topMotm:
        df.at[5, "Punten"] = 5
        total_points += 5
    if df.at[6, "Antwoord"] in topCards:
        df.at[6, "Punten"] = 5
        total_points += 5
    diff = abs(cleanSheets - int(df.at[7, "Antwoord"]))
    if diff < 5:
        df.at[7, "Punten"] = 5 - diff
        total_points += 5 - diff

    print(df)
    with open(output_html, 'a') as f:
            f.write(df.to_html(index=False))
            f.write("</br>")

    data = [total_points]
    df = pd.DataFrame(data)
    df.index = ["punten totaal"]

    ranking.append([name, total_points])

    print(df)
    with open(output_html, 'a') as f:
            f.write(df.to_html(header=False))
            f.write("</br>")


sorted_list = sorted(ranking, key=lambda x:x[1], reverse=True)

index_html = """
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Rank</th>
      <th>Naam</th>
      <th>Punten</th>
    </tr>
  </thead>
  <tbody>
"""
for c, i in enumerate(sorted_list):
    index_html += f"""
    <tr style="text-align: right;">
        <td>#{c+1}</td>
        <td><a href="voorspellingen/{i[0]}.html">{i[0]}</a></td>
        <td>{i[1]}</td>
    </tr>
    """
index_html +="""
    </tbody>
</table>
"""
with open("index.html", 'w') as f:
    f.write(index_html)
    f.write("</br>")

