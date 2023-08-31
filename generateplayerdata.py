
players = [
    "Olivier Abee",
    "Jonas Abee",
    "Tycho Berend",
    "Olivier van den Bergh",
    "Siep Böhmer",
    "Sander van Duffelen",
    "Hidde Frenk",
    "Wessel Gratama van Andel",
    "Laurens van Hooft",
    "Rinse Kloek",
    "Matthijs Koenst",
    "Bart Laoh",
    "Joost Laoh",
    "Daniel van Liempd",
    "Gijs Loke",
    "Mees Roosen",
    "Milan Staring",
    "Maurits van den Tweel",
    "Team Invallers"
]
playerdata = []
for player in players:
    playerdata.append({"name": player, "data": {"goals": 0, "assists": 0, "kaarten": 0, "motm": 0}})

import json
json.dump(playerdata, open("playerdata.json", "w"), indent=4)