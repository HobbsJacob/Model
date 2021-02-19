import os
import json

uniqePos = []

for fname in os.listdir("playerData"):
    with open(os.path.join("playerData", fname), "r") as file:
        j = json.load(file)
        for player in j["players"]:
            if player["playerDetails"]["position"] not in uniqePos:
                uniqePos.append(player["playerDetails"]["position"])

print(uniqePos)
