import json
import os
import sys

class Team:
    def __init__(self, n, sid):
        self.name = n
        self.squadId = sid
        self.previousStats = {}         # Dict
        self.currentSeason = 0
        self.currentGame = 1

    def printStats(self):
        out = ""
        for key,val in self.previousStats.items():
            out += str(val) + ","

        return out[:-1]

    def updateValues(self, data):

        if self.previousStats == {}:
            for team in j["matchStats"]["teamStats"]["team"]:
                if team["squadId"] == self.squadId:
                    for key, val in team.items():
                        self.previousStats[key] = float(val)


            distance = [0, 0, 0, 0]
            missedDistance = [0, 0, 0, 0]

            for section in data["matchStats"]["scoreFlow"]["score"]:
                if section["squadId"] == self.squadId:
                    if section["scoreName"] == "goal":
                        distance[section["distanceCode"]] += 1
                    else:
                        missedDistance[section["distanceCode"]] += 1

            for i in range(0, 4):
                self.previousStats["hit" + str(i)] = distance[i]
                self.previousStats["miss" + str(i)] = missedDistance[i]


            return

        for team in j["matchStats"]["teamStats"]["team"]:
            if team["squadId"] == self.squadId:
                for key, val in team.items():
                    self.previousStats[key] = (self.previousStats[key] * 0.1) + (float(val) * 0.9)


        distance = [0,0,0,0]
        missedDistance = [0,0,0,0]

        for section in data["matchStats"]["scoreFlow"]["score"]:
            if section["squadId"] == self.squadId:
                if section["scoreName"] == "goal":
                    distance[section["distanceCode"]] += 1
                else:
                    missedDistance[section["distanceCode"]] += 1

        for i in range(0,4):
            self.previousStats["hit" + str(i)] = self.previousStats["hit" + str(i)] * 0.2 + distance[i] * 0.8
            self.previousStats["miss" + str(i)] = self.previousStats["miss" + str(i)] * 0.2 + missedDistance[i] * 0.8





allTeams = {}
allTeams["Steel"] = Team("Steel", 808)
allTeams["Stars"] = Team("Stars", 8120)
allTeams["Magic"] = Team("Magic", 809)
allTeams["Tactix"] = Team("Tactix", 802)
allTeams["Mystics"] = Team("Mystics", 805)
allTeams["Pulse"] = Team("Pulse", 803)

with open("out.csv", "w") as outfile:
    outfile.write("home,away,rea,gfcpa,gfta,pa,tipa,ga,posa,oraa,gma,1,2,3,4,5,6,7,8,9,0,11,12,13,14,15,ba,passa,gaa,da,tuwa,cpra,opa,fea,goalsa,offa,badpa,dra,breaka,blocka,badha,mgta,gfga,sia,goalaa,deflaa,cpa,turna,picka,intera,rb,gfcpb,gftb,penb,tipb,gainb,possb,orb,gmb,bb,passb,gasdfb,dispb,tuwb,cprb,opb,feedb,goalsb,offb,bpb,drb,breakb,blockb,bhb,mgtb,gfgb,sib,gab,deflb,turnb,pickb,interb,h0,m0,h1,m1,h2,m2,h3,m3,,one,two,three,four,five,six,seven,eight,result\n")

    for f in os.listdir("json"):
        with open(os.path.join("json", f), "r") as file:
            line = ""
            j = json.loads(file.read().encode('utf-8'))

            home_team = j["matchStats"]["teamInfo"]["team"][0]["squadNickname"]
            away_team = j["matchStats"]["teamInfo"]["team"][1]["squadNickname"]

            if len(allTeams[home_team].previousStats) == 0:
                allTeams[home_team].updateValues(j)
            if len(allTeams[away_team].previousStats) == 0:
                allTeams[away_team].updateValues(j)

            line += home_team + "," + away_team + ","

            line += allTeams[home_team].printStats() + ","
            line += allTeams[away_team].printStats() + ","

            result = ""



            if j["matchStats"]["teamStats"]["team"][0]["goals"] > j["matchStats"]["teamStats"]["team"][1]["goals"]:
                result = "WIN"
            else:
                result = "LOSS"

            line += result

            outfile.write(line + "\n")

            allTeams[home_team].updateValues(j)
            allTeams[away_team].updateValues(j)

