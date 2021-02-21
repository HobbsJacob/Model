import itertools
import math
import os
import json
import requests
import sys
from math import sqrt
from trueskill import Rating, BETA, global_env, rate_1vs1, TrueSkill
from trueskill.backends import cdf





headers = {'x-media-mis-token': '7dadaab360b55276c9d5508f5f470d0a'} #API key

FADE = 0.6                              #Fading factor for stats each week

env = TrueSkill(draw_probability=0)
env.make_as_global()                    #elo set up

home_advantage = Rating()               #A player on the home team

def win_probability(team1, team2):                                          #Copy pasted off the innernet
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    return cdf(delta_mu / denom)


class Team:
    def __init__(self, name):               #Team has a name, and players
        self.name = name
        self.players = {}

    def addPlayer(self, pName):
        self.players[pName] = Player(pName) #Create an empty player and put it in the dict

    def printStats(self, players):                                  #create a string of comma seperated stats
        for p in players:
            if p["playerId"] not in self.players:                   #ONLY IF THIS IS A NEW PLAYER, tested and this condition works, no cheating here
                self.players[p["playerId"]] = Player(p["playerId"])
                self.players[p["playerId"]].updatePlayerStats(p)    #Create it, and then update only this player with 'future stats'


        return self.printPositionStats(players)                     #Go to the actual print stats function

    def updateStats(self, players):                             #update all players in the game
        for p in players:
            if p["playerId"] not in self.players:

                self.players[p["playerId"]] = Player(p["playerId"])         #If this player is new, make a new player for it.

            self.players[p["playerId"]].updatePlayerStats(p)                #update this player

    def printPositionStats(self, players):      #PLAYERS HERE IS DANGEROUS
        tempP = {}                              #tempP[position][stat]
        posTime = {}                            #Get a total time for each position
        for pos in positions:
            tempP[pos] = {}
            for stat in statOrder:
                tempP[pos][stat] = 0            #Fill out the output stats for this team as zero (prevents error for missing stats)
            posTime[pos] = 0






        for player in players:                                                                                      #Find the total time on ground of PREVIOUS GAMES
            posTime[player["playerDetails"]["position"]] = posTime[player["playerDetails"]["position"]] + self.players[player["playerId"]].stats["timeOnGroundPercentage"]  #Add the previous time on ground to the total for their position

        for player in players:

            percentage = 0      #The time on field percentage with respect to the total for their position

            if posTime[player["playerDetails"]["position"]] != 0:   #If they were on the field, set their percentage as their time / total for the position
                percentage = self.players[player["playerId"]].stats["timeOnGroundPercentage"] / posTime[player["playerDetails"]["position"]]

            #Begin collecting the stats for each position to output into tempP

            if len(tempP[player["playerDetails"]["position"]]) == 0:                        #If there are no collected stats in this position yet
                for stat, val in self.players[player["playerId"]].stats.items():            #Access the PAST DATA
                    if stat != "matchesPlayed":
                        tempP[player["playerDetails"]["position"]][stat] = val * percentage #Set the output of this stat = to the PAST DATA value * it's time percentage
            else:                                                                           #Else stats for this position exist
                for stat, val in self.players[player["playerId"]].stats.items():            #NICE PAST DATA
                    if stat != "matchesPlayed":
                        tempP[player["playerDetails"]["position"]][stat] = tempP[player["playerDetails"]["position"]][stat] + (val * percentage)    #Add the new stat to the current collection

        out = []        #Next bit just converts tempP into comma seperated string

        for item in positions:
            for s in statOrder:
                try:
                    out.append(str(tempP[item][s]))
                except:
                    print(tempP)
                    exit(0)

        return ",".join(out)        #return the string


class Player:                       #A single player, has an id, past stats and an elo skill
    def __init__(self, id):
        self.id = id
        self.stats = {}
        self.skill = Rating()       #Give it an empty elo

    def updatePlayerStats(self, stats):     #Given future stats, update the old ones for this player
        if len(self.stats) == 0:            #If this player has no stats yet
            for stat in statOrder:
                self.stats[stat] = 0        #Set them all to zero

            for stat, val in stats["totals"].items():   #Set this players stats = to the future data
                self.stats[stat] = float(val)

        else:                                           #Update the old stats to new ones with the fading factor
            for stat, val in stats["totals"].items():
                self.stats[stat] = self.stats[stat] * (1-FADE) + val * FADE





#Set up empty teams

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

#All positions
positions = ['MEDIUM_DEFENDER', 'MIDFIELDER', 'KEY_DEFENDER', 'RUCK', 'MEDIUM_FORWARD', 'MIDFIELDER_FORWARD', 'KEY_FORWARD']

#All stats and the order they should be output
statOrder = ["timeOnGroundPercentage","behinds","bounces","centreClearances","clangers","contestDefLosses","contestDefLossPercentage","contestDefOneOnOnes","contestedMarks","contestedPossessionRate","contestedPossessions","contestOffOneOnOnes","contestOffWins","contestOffWinsPercentage","defHalfPressureActs","disposalEfficiency","disposals","dreamTeamPoints","effectiveDisposals","effectiveKicks","f50GroundBallGets","freesAgainst","freesFor","goalAccuracy","goalAssists","goals","groundBallGets","handballs","hitouts","hitoutsToAdvantage","hitoutToAdvantageRate","hitoutWinPercentage","inside50s","interceptMarks","intercepts","kickEfficiency","kicks","kickToHandballRatio","marks","marksInside50","marksOnLead","metresGained","onePercenters","pressureActs","ratingPoints","rebound50s","ruckContests","scoreInvolvements","scoreLaunches","shotsAtGoal","spoils","stoppageClearances","tackles","tacklesInside50","totalClearances","totalPossessions","turnovers","uncontestedPossessions"]



#Open the output file
with open("playerParsed.csv", "w") as outFile:

    header = ""

    #write the column names

    for x in positions:
        for y in statOrder:
            header += "h" + x + y + ","
    for x in positions:
        for y in statOrder:
            header += "a" + x + y + ","
    header += "result\n"

    outFile.write(header)


    #Get the gamecodes from the whole game data files
    for f in os.listdir("data"):
        #Open the whole match data, though we never use it
        with open(os.path.join("data", f), "r") as matchData:
            #Open the player data
            with open(os.path.join("playerData", f), "r") as playerData:
                line = ""
                currentGameData = json.load(playerData)
                pM = json.load(matchData)

                homeTeam = ""
                awayTeam = ""

                try:  # Get results

                    #Don't know why I fetch it again when I literally already have the file opened but oh well
                    page = requests.get("https://api.afl.com.au/cfs/afl/matchRoster/full/" + f, headers=headers)


                    j = json.loads(page.text)
                    homeTeam = j["match"]["homeTeam"]["name"]                                                           #Get team names
                    awayTeam = j["match"]["awayTeam"]["name"]

                    homeScore = j["matchRoster"]["recentMatches"][0]["homeResult"]["scoreBreakdown"]["totalScore"]      #Get their scores
                    awayScore = j["matchRoster"]["recentMatches"][0]["awayResult"]["scoreBreakdown"]["totalScore"]


                    homePlayers = []        #Start collecting the players that played in this game
                    awayPlayers = []

                    home_ratings = []       #Used to adjust elo LATER
                    away_ratings = []
                    hdict = {}
                    adict = {}

                    for player in currentGameData["players"]:               #Go through each player and put them in their team
                        if player["team"]["teamName"] == homeTeam:
                            homePlayers.append(player)
                        else:
                            awayPlayers.append(player)

                    line += allTeams[homeTeam].printStats(homePlayers) + ","        #Add the PAST STATS to the output line
                    line += allTeams[awayTeam].printStats(awayPlayers) + ","

                    allTeams[homeTeam].updateStats(homePlayers)                     #Now update the stats
                    allTeams[awayTeam].updateStats(awayPlayers)

                    if homeScore - awayScore > 0:                                   #Add the game result to the line
                        line += "win,"
                    else:
                        line += "loss,"

                    time_weights = {}           #Collect time on field weights as a contribution to the result for adjusting elo

                    for player in homePlayers:                                                             #For each player
                        home_ratings.append(allTeams[homeTeam].players[player["playerId"]].skill)          #Get it's elo object into a list for win %
                        hdict[player["playerId"]] = allTeams[homeTeam].players[player["playerId"]].skill   #And then also into a dictionary for updating
                        time_weights[(0, player["playerId"])] = player["totals"]["timeOnGroundPercentage"] #Use 'future' time on field for the current game to weight their elo adjustment, it isn't used in win% so it's fine

                    for player in awayPlayers:                                                              #same again for away team
                        away_ratings.append(allTeams[awayTeam].players[player["playerId"]].skill)
                        adict[player["playerId"]] = allTeams[awayTeam].players[player["playerId"]].skill
                        time_weights[(1, player["playerId"])] = player["totals"]["timeOnGroundPercentage"]

                    line += str(win_probability(home_ratings, away_ratings))                                #Use only the lists of rating objects above to add the win% to the line

                    line += "\n"
                    outFile.write(line)                                                                     #write out the line, donezo















                    hdict["home_advantage"] = home_advantage                                                #Add the home advantage player to the home team
                    rating_groups = [hdict, adict]

                    rated_rating_groups = 0





                    if homeScore - awayScore > 0:                                                           #Update the elo based on the result and the weights
                        rated_rating_groups = env.rate(rating_groups, ranks=[0, 1], weights=time_weights)
                    else:
                        rated_rating_groups = env.rate(rating_groups, ranks=[1, 0], weights=time_weights)



                    for key, val in rated_rating_groups[0].items():         #For home player that played
                        if key == "home_advantage":
                            home_advantage = val                            #Update home advantage elo
                        else:
                            allTeams[homeTeam].players[key].skill = val     #Set their skill to the updated one
                    for key, val in rated_rating_groups[1].items():         #Then away
                        allTeams[awayTeam].players[key].skill = val
                    print(f)                                                #Print progress



                except():
                    print("whoops")







