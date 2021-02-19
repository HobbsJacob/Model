import itertools
import math
import os
import json
import requests
import sys
from math import sqrt
from trueskill import Rating, BETA, global_env, rate_1vs1, TrueSkill
from trueskill.backends import cdf

headers = {'x-media-mis-token': 'd5a21a4ba3894b84729d1f58a34bfe36'}

FADE = 0.6

env = TrueSkill(draw_probability=0)
env.make_as_global()

def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    return cdf(delta_mu / denom)


class Team:
    def __init__(self, name):
        self.name = name
        self.players = {}

    def addPlayer(self, pName):
        self.players[pName] = Player(pName)

    def printStats(self, players):
        for p in players:
            if p["playerId"] not in self.players:
                self.players[p["playerId"]] = Player(p["playerId"])
                self.players[p["playerId"]].updatePlayerStats(p)
        return self.printPositionStats(players)

    def updateStats(self, players):
        for p in players:
            if p["playerId"] not in self.players:

                self.players[p["playerId"]] = Player(p["playerId"])         #If this player is new, make a new player for it.

            self.players[p["playerId"]].updatePlayerStats(p)


    def printAllStats(self, players):
        pass

    def printPositionStats(self, players):      #PLAYERS HERE IS DANGEROUS
        tempP = {}          #tempP[position][stat]
        posTime = {}
        for pos in positions:
            tempP[pos] = {}
            for stat in statOrder:
                tempP[pos][stat] = 0
            posTime[pos] = 0




        for player in players:          #Find the total time on ground of PREVIOUS GAMES
            posTime[player["playerDetails"]["position"]] = posTime[player["playerDetails"]["position"]] + self.players[player["playerId"]].stats["timeOnGroundPercentage"]

        for player in players:

            percentage = 0

            if posTime[player["playerDetails"]["position"]] != 0:
                percentage = self.players[player["playerId"]].stats["timeOnGroundPercentage"] / posTime[player["playerDetails"]["position"]]

            if len(tempP[player["playerDetails"]["position"]]) == 0:                        #If there are no stats in this position yet
                for stat, val in self.players[player["playerId"]].stats.items():
                    if stat != "matchesPlayed":
                        tempP[player["playerDetails"]["position"]][stat] = val * percentage
            else:
                for stat, val in self.players[player["playerId"]].stats.items():
                    if stat != "matchesPlayed":
                        tempP[player["playerDetails"]["position"]][stat] = tempP[player["playerDetails"]["position"]][stat] + (val * percentage)

        out = []

        for item in positions:
            for s in statOrder:
                try:
                    out.append(str(tempP[item][s]))
                except:
                    print(tempP)
                    exit(0)

        return ",".join(out)


class Player:
    def __init__(self, id):
        self.id = id
        self.stats = {}
        self.skill = Rating()

    def updatePlayerStats(self, stats):
        if len(self.stats) == 0:
            for stat in statOrder:
                self.stats[stat] = 0

            for stat, val in stats["totals"].items():
                self.stats[stat] = float(val)

        else:
            for stat, val in stats["totals"].items():
                try:
                    self.stats[stat] = self.stats[stat] * (1-FADE) + val * FADE
                except:
                    print(self.id)
                    print(self.stats)
                    exit(0)
                    print(stat)






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

positions = ['MEDIUM_DEFENDER', 'MIDFIELDER', 'KEY_DEFENDER', 'RUCK', 'MEDIUM_FORWARD', 'MIDFIELDER_FORWARD', 'KEY_FORWARD']

statOrder = ["timeOnGroundPercentage","behinds","bounces","centreClearances","clangers","contestDefLosses","contestDefLossPercentage","contestDefOneOnOnes","contestedMarks","contestedPossessionRate","contestedPossessions","contestOffOneOnOnes","contestOffWins","contestOffWinsPercentage","defHalfPressureActs","disposalEfficiency","disposals","dreamTeamPoints","effectiveDisposals","effectiveKicks","f50GroundBallGets","freesAgainst","freesFor","goalAccuracy","goalAssists","goals","groundBallGets","handballs","hitouts","hitoutsToAdvantage","hitoutToAdvantageRate","hitoutWinPercentage","inside50s","interceptMarks","intercepts","kickEfficiency","kicks","kickToHandballRatio","marks","marksInside50","marksOnLead","metresGained","onePercenters","pressureActs","ratingPoints","rebound50s","ruckContests","scoreInvolvements","scoreLaunches","shotsAtGoal","spoils","stoppageClearances","tackles","tacklesInside50","totalClearances","totalPossessions","turnovers","uncontestedPossessions"]




with open("playerParsed.csv", "w") as outFile:

    header = ""

    for x in positions:
        for y in statOrder:
            header += "h" + x + y + ","
    for x in positions:
        for y in statOrder:
            header += "a" + x + y + ","
    header += "result\n"

    outFile.write(header)

    for f in os.listdir("data"):
        with open(os.path.join("data", f), "r") as matchData:
            with open(os.path.join("playerData", f), "r") as playerData:
                line = ""
                pP = json.load(playerData)
                pM = json.load(matchData)

                homeTeam = ""
                awayTeam = ""

                try:  # Get results
                    page = requests.get("https://api.afl.com.au/cfs/afl/matchRoster/full/" + f, headers=headers)


                    j = json.loads(page.text)
                    homeTeam = j["match"]["homeTeam"]["name"]
                    awayTeam = j["match"]["awayTeam"]["name"]

                    homeScore = j["matchRoster"]["recentMatches"][0]["homeResult"]["scoreBreakdown"]["totalScore"]
                    awayScore = j["matchRoster"]["recentMatches"][0]["awayResult"]["scoreBreakdown"]["totalScore"]


                    homePlayers = []
                    awayPlayers = []

                    home_ratings = []
                    away_ratings = []
                    hdict = {}
                    adict = {}

                    for player in pP["players"]:
                        if player["team"]["teamName"] == homeTeam:
                            homePlayers.append(player)
                        else:
                            awayPlayers.append(player)

                    line += allTeams[homeTeam].printStats(homePlayers) + ","
                    line += allTeams[awayTeam].printStats(awayPlayers) + ","

                    allTeams[homeTeam].updateStats(homePlayers)
                    allTeams[awayTeam].updateStats(awayPlayers)

                    if homeScore - awayScore > 0:
                        line += "win,"
                    else:
                        line += "loss,"

                    time_weights = {}

                    for player in homePlayers:
                        home_ratings.append(allTeams[homeTeam].players[player["playerId"]].skill)
                        hdict[player["playerId"]] = allTeams[homeTeam].players[player["playerId"]].skill
                        time_weights[(0, player["playerId"])] = player["totals"]["timeOnGroundPercentage"]

                    for player in awayPlayers:
                        away_ratings.append(allTeams[awayTeam].players[player["playerId"]].skill)
                        adict[player["playerId"]] = allTeams[awayTeam].players[player["playerId"]].skill
                        time_weights[(1, player["playerId"])] = player["totals"]["timeOnGroundPercentage"]

                    line += str(win_probability(home_ratings, away_ratings))

                    line += "\n"
                    outFile.write(line)

                    rating_groups = [hdict, adict]

                    rated_rating_groups = 0





                    if homeScore - awayScore > 0:
                        rated_rating_groups = env.rate(rating_groups, ranks=[0, 1], weights=time_weights)
                    else:
                        rated_rating_groups = env.rate(rating_groups, ranks=[1, 0])

                    for key, val in rated_rating_groups[0].items():
                        allTeams[homeTeam].players[key].skill = val
                    for key, val in rated_rating_groups[1].items():
                        allTeams[awayTeam].players[key].skill = val
                    print(f)
                except():
                    pass







