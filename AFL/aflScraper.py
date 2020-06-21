import requests
import os

headers = {'x-media-mis-token': '98cdab6de2db279ff3aefa1df0535ac5'}





season = "CD_M2015014"
week = 1
game = 1

while 0 == 0:
    gameCode = season + str(week).zfill(2) + str(game).zfill(2)
    page = requests.get("https://api.afl.com.au/cfs/afl/teamStats/match/" + gameCode, headers=headers)

    print(gameCode)

    if len(page.text) < 40:  # Fail
        if game == 1:
            exit(0)
        week += 1
        game = 1
    else:
        with open(os.path.join("data", gameCode), "wb") as file:
            file.write(page.content)


        game += 1
