import requests
import pprint

class Api:
    base_url = "https://publicaties.hockeyweerelt.nl"
    headers = {
        "Accept": "application/json"
    }
    def get_clubs(self):
        r = requests.get(f"{self.base_url}/mc/clubs", headers=self.headers)
        return r.json()["data"]
    
    def get_club_info(self, club): # untested
        r = requests.get(f"{self.base_url}/mc/clubs/{club}", headers=self.headers)
        return r.json()["data"]

    def get_club_teams(self, club):
        r = requests.get(f"{self.base_url}/mc/clubs/{club}/teams", headers=self.headers)
        return r.json()["data"]
    
    def get_team_info(self, team):
        r = requests.get(f"{self.base_url}/mc/teams/{team}", headers=self.headers)
        return r.json()["data"]
    
    def get_team_matches(self, team, competition):
        page = 0
        target = 1
        params = {
            "competition_id": competition,
            "show_all": 1 
        }
        all_matches = []
        while page < target+1:
            params["page"] = page
            page+=1
            
            r = requests.get(f"{self.base_url}/mc/teams/{team}/matches/upcoming", params=params, headers=self.headers)
            requestData = r.json()
            all_matches += requestData["data"]
            target = requestData["meta"]["last_page"]

        return all_matches
    
    def get_standing(self, competition):
        r = requests.get(f"{self.base_url}/mc/competitions/{competition}/standing")
        return r.json()["data"]

    def get_results(self, teams, competition):
        r = requests.get(f"{self.base_url}/mc/teams/{teams}/matches/official?=&competition_id={competition}&show_all=0")
        return r.json()["data"]
        
