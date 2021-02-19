import requests
import os

headers = {'x-media-mis-token': '094342312a2c0d823e18df7c43a07264'}




season = "CD_M2020014"
week = 1
game = 1

already = os.listdir("data")

while 0 == 0:
    gameCode = season + str(week).zfill(2) + str(game).zfill(2)

    if gameCode not in already:
        page = requests.get("https://api.afl.com.au/cfs/afl/teamStats/match/" + gameCode, headers=headers)

        print(gameCode)

        if len(page.text) < 40:  # Fail
            if game == 1:
                exit(0)
            week += 1
            game = 0
        else:
            with open(os.path.join("data", gameCode), "wb") as file:
                file.write(page.content)


    game += 1
