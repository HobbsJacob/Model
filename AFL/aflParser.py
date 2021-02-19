import os
import json
import requests
import sys
from math import sqrt
from trueskill import Rating, BETA, global_env, rate_1vs1, TrueSkill
from trueskill.backends import cdf

headers = {'x-media-mis-token': '094342312a2c0d823e18df7c43a07264'}

env = TrueSkill(draw_probability=0)
env.make_as_global()

def win_probability(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)

class Team:
    naughtyWords = ["superGoals", "ratingPoints", "ranking", "lastUpdated", "scoreInvolvements", "metresGained","scoreDiff","previousTeam"]
    skill = Rating()
    def __init__(self, n):
        self.name = n
        self.previousStats = {}         # Dict

    def printStats(self):
        out = ""
        for key,val in self.previousStats.items():
            if key not in self.naughtyWords:
                out += str(val) + ","

        return out[:-1]

    def updateValues(self, data):

        if self.previousStats == {}:
            for key, val in data.items():
                if key not in self.naughtyWords:
                    if key == "clearances":
                        self.previousStats["centreClearances"] = val["centreClearances"]
                        self.previousStats["stoppageClearances"] = val["stoppageClearances"]

                    elif key == "interchangeCounts":
                        self.previousStats["interchangeCountQ1"] = val["interchangeCountQ1"]
                        self.previousStats["interchangeCountQ2"] = val["interchangeCountQ2"]
                        self.previousStats["interchangeCountQ3"] = val["interchangeCountQ3"]
                        self.previousStats["interchangeCountQ4"] = val["interchangeCountQ4"]
                    else:
                        self.previousStats[key] = float(val)
            self.previousStats["scoreDiff"] = 0
            self.previousStats["previousTeam"] = ""
            return


        for key,val in data.items():
            if key not in self.naughtyWords:
                if key == "clearances":
                    self.previousStats["centreClearances"] = (self.previousStats["centreClearances"] * 0.2) + (float(val["centreClearances"]))
                    self.previousStats["stoppageClearances"] = (self.previousStats["stoppageClearances"] * 0.2) + (float(val["stoppageClearances"]))

                elif key == "interchangeCounts":
                    self.previousStats["interchangeCountQ1"] = (self.previousStats["interchangeCountQ1"] * 0.2) + (float(val["interchangeCountQ1"]))
                    self.previousStats["interchangeCountQ2"] = (self.previousStats["interchangeCountQ2"] * 0.2) + (float(val["interchangeCountQ2"]))
                    self.previousStats["interchangeCountQ3"] = (self.previousStats["interchangeCountQ3"] * 0.2) + (float(val["interchangeCountQ3"]))
                    self.previousStats["interchangeCountQ4"] = (self.previousStats["interchangeCountQ4"] * 0.2) + (float(val["interchangeCountQ4"]))
                else:
                    try:
                        self.previousStats[key] = (self.previousStats[key] * 0.2) + (float(val) * 0.8)
                    except:
                        print(sys.exc_info())
                        print("failed " + key)


allTeams = {}
allTeams["Geelong Cats"] = Team("Geelong Cats")
allTeams["Brisbane Lions"] = Team("Brisbane Lions")
allTeams["Richmond"] = Team("Richmond")
allTeams["Collingwood"] = Team("Collingwood")
allTeams["West Coast Eagles"] = Team("West Coast Eagles")
allTeams["GWS Giants"] = Team("GWS Giants")
allTeams["Western Bulldogs"] = Team("Western Bulldogs")
allTeams["Essendon"] = Team("Essendon")
allTeams["Hawthorn"] = Team("Hawthorn")
allTeams["Port Adelaide"] = Team("Port Adelaide")
allTeams["Adelaide Crows"] = Team("Adelaide Crows")
allTeams["North Melbourne"] = Team("North Melbourne")
allTeams["Fremantle"] = Team("Fremantle")
allTeams["St Kilda"] = Team("St Kilda")
allTeams["Carlton"] = Team("Carlton")
allTeams["Sydney Swans"] = Team("Sydney Swans")
allTeams["Melbourne"] = Team("Melbourne")
allTeams["Gold Coast Suns"] = Team("Gold Coast Suns")

with open("parsed.csv", "w") as outFile:
    outFile.write("home,away,percent,aaa,aab,aac,aad,aae,aaf,aag,aah,aai,aaj,aak,aal,zzzz,aam,aan,aao,aap,aaq,aar,aas,aat,aau,aav,aaw,aax,aay,aaz,aba,aca,ada,aea,afa,aga,aha,aia,aja,aka,ala,ama,ana,aoa,apa,aqa,ara,asa,ata,aua,ava,awa,axa,aya,aza,baa,caa,daa,eaa,faa,gaa,haa,iaa,jaa,kaa,laa,maa,naa,oaa,paa,qaa,raa,saa,taa,uaa,vaa,waa,xaa,ptpa,ptpb,Result\n")
    for jFile in os.listdir("data"):
        with open(os.path.join("data", jFile), "r") as file:
            print(jFile)
            line = ""
            j = json.load(file)

            home = j["teamStats"][0]["teamName"]["teamName"]
            away = j["teamStats"][1]["teamName"]["teamName"]


                                                                                #Empty stats
            if allTeams[home].previousStats == {}:
                allTeams[home].updateValues(j["teamStats"][0]["stats"])

            if allTeams[away].previousStats == {}:
                allTeams[away].updateValues(j["teamStats"][1]["stats"])

            line += home + "," + away + ","

            line += str(win_probability(allTeams[home].skill, allTeams[away].skill)) + ","                                                                    #Add trueskill


            line += allTeams[home].printStats() + ","                          #Print stats
            line += allTeams[away].printStats() + ","

            allTeams[home].updateValues(j["teamStats"][0]["stats"])             #Update stats
            allTeams[away].updateValues(j["teamStats"][1]["stats"])
            try:                                                                                                        #Get results
                page = requests.get("https://api.afl.com.au/cfs/afl/matchRoster/full/" + jFile, headers=headers)

                j = json.loads(page.text)

                line += j["venue"]["abbreviation"] + ","

                homeScore = j["matchRoster"]["recentMatches"][0]["homeResult"]["scoreBreakdown"]["totalScore"]
                awayScore = j["matchRoster"]["recentMatches"][0]["awayResult"]["scoreBreakdown"]["totalScore"]

                line += str(allTeams[home].previousStats["scoreDiff"]) + "," + str(allTeams[away].previousStats["scoreDiff"]) + ","

                allTeams[home].previousStats["scoreDiff"] = allTeams[home].previousStats["scoreDiff"] * 0.2 + (homeScore - awayScore) * 0.8
                allTeams[away].previousStats["scoreDiff"] = allTeams[away].previousStats["scoreDiff"] * 0.2 + (awayScore - homeScore) * 0.8

                line += allTeams[home].previousStats["previousTeam"] + "," + allTeams[away].previousStats["previousTeam"] + ","

                allTeams[home].previousStats["previousTeam"] = away

                allTeams[away].previousStats["previousTeam"] = home

                if homeScore - awayScore > 0:
                    line += "win"
                    allTeams[home].skill, allTeams[away].skill = rate_1vs1(allTeams[home].skill, allTeams[away].skill)
                else:
                    line += "loss"
                    allTeams[away].skill, allTeams[home].skill = rate_1vs1(allTeams[away].skill,
                                                                                     allTeams[home].skill)

                line += "\n"

            except:
                print("errored")
                print(sys.exc_info())

                line += "VENUE" + ","

                line += str(allTeams[home].previousStats["scoreDiff"]) + "," + str(
                    allTeams[away].previousStats["scoreDiff"]) + ","

                line += allTeams[home].previousStats["previousTeam"] + "," + allTeams[away].previousStats[
                    "previousTeam"] + ","

                line += "win"

                line += "\n"

            outFile.write(line)

#I don't think the values are being updated properly there aren't any massive decimal points anywhere




















