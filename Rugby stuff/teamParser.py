import json
import os
import sys



#             Player[]        each player in the team
#                 PlayerStats{}
#                     PlayerStat[]        Their stats
#                         @value     blank
#                         @attributes
#                             "stat name":value
#                 @attributes
#                     id
#                     player_name
#                     position
#                     position_id



class Team:
    def __init__(self, n):
        self.name = n
        self.previousStats = {}         # Dict
        self.currentSeason = 0
        self.currentGame = 1

        self.players = {}

    def printStats(self, data):
        #If we don't have it then update it, print position id
        out = ""
        for player in data:
            name = player["@attributes"]["player_name"]
            position = player["@attributes"]["position_id"]

            out += name + "," + position + ","

            if name not in self.players:
                self.players[name] = {}
                for stat in player["PlayerStats"]["PlayerStat"]:
                    key = str(list(stat["@attributes"])[0])
                    val = float(stat["@attributes"][key])
                    self.players[name][key] = val

            for key,val in self.players[name].items():
                out += str(val) + ","

        return out[:-1]

    def updateValues(self, data):
        for player in data:
            name = player["@attributes"]["player_name"]
            if name not in self.players:
                self.players[name] = {}
                for stat in player["PlayerStats"]["PlayerStat"]:
                    key = str(list(stat["@attributes"])[0])
                    val = float(stat["@attributes"][key])
                    self.players[name][key] = val
            else:
                for stat in player["PlayerStats"]["PlayerStat"]:
                    key = str(list(stat["@attributes"])[0])
                    val = float(stat["@attributes"][key])
                    self.players[name][key] = val * 0.8 + self.players[name][key] * 0.2





# conceded, name, home/a

allTeams = {}
allTeams["Lions"] = Team("Lions")
allTeams["Highlanders"] = Team("Highlanders")
allTeams["Reds"] = Team("Reds")
allTeams["Bulls"] = Team("Bulls")
allTeams["Hurricanes"] = Team("Hurricanes")
allTeams["Chiefs"] = Team("Chiefs")
allTeams["Rebels"] = Team("Rebels")
allTeams["Jaguares"] = Team("Jaguares")
allTeams["Waratahs"] = Team("Waratahs")
allTeams["Stormers"] = Team("Stormers")
allTeams["Sharks"] = Team("Sharks")
allTeams["Blues"] = Team("Blues")
allTeams["Sunwolves"] = Team("Sunwolves")
allTeams["Crusaders"] = Team("Crusaders")
allTeams["Brumbies"] = Team("Brumbies")

def parse_file(name):                                                                                           # For each file
    with open(os.path.join("datas", name)) as file:

        text = file.read()                                                                                      # Read it

        text = text[:-1]
        text = text[11:]
        text = text.replace("NSW Waratahs", "Waratahs")
        if "Force" in text or "Cheetahs" in text or "\"team_name\":\"Kings\"" in text:
            return



        #############################################################FIRST RUN                                                                          #if this is the first game, update values right now
        j = json.loads(text)
        line = ""
        try:
            if len(allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].previousStats.items()) == 0:
                allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].updateValues(
                    j["RRML"]["TeamDetail"]["Team"][0]["Player"])



            if allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].previousStats == {}:
                allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].updateValues(
                    j["RRML"]["TeamDetail"]["Team"][1]["Player"])
        except:
            print(sys.exc_info())


        #########################################################################

        home = j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]               #known pre game
        away = j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]


        line += home + ","
        line += away + ","
        line += j["RRML"]["@attributes"]["season_id"] + ","                                 #known pre game


        line += allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].printStats(j["RRML"]["TeamDetail"]["Team"][0]["Player"]) + ","         #print stats
        line += allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].printStats(j["RRML"]["TeamDetail"]["Team"][1]["Player"]) + ","



        ########## Score                                                                                #NOT PRE GAME, BUT WE ARE GUESSING THIS
        if j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["home_or_away"] == "home":
            if j["RRML"]["@attributes"]["away_score"] >= j["RRML"]["@attributes"]["home_score"]:
                line += "LOSS"
            else:
                line += "WIN"
        else:
            if j["RRML"]["@attributes"]["away_score"] <= j["RRML"]["@attributes"]["home_score"]:
                line += "LOSS"
            else:
                line += "WIN"

        outfile.write(line + "\n")                                                                  #HERE THE LINE IS WRITTEN, NO UPDATING BEFORE THIS LINE

        allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].updateValues(
            j["RRML"]["TeamDetail"]["Team"][0]["Player"])

        allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].updateValues(
            j["RRML"]["TeamDetail"]["Team"][1]["Player"])



with open("out.csv", "w") as outfile:
    for path in os.listdir("datas"):
        parse_file(path)



# RRML
#     Events
#         Event[]
#             @attributes
#                 minute
#                 period
#                 player_id
#                 second
#                 team_id
#                 type
#     Officials
#         Official[]
#             @value
#             @attributes
#                 id
#                 country
#                 official_name
#                 role
#     TeamDetail
#         Team[]     each team
#             Player[]        each player in the team
#                 PlayerStats{}
#                     PlayerStat[]        Their stats
#                         @value     blank
#                         @attributes
#                             "stat name":value
#                 @attributes
#                     id
#                     player_name
#                     position
#                     position_id
#             TeamStats
#                 TeamStat[]
#                     @value    blank
#                     @attributes
#                         "stat name":value
#             @attributes
#                 home_or_away
#                 team_id
#                 team_name
#     @attributes