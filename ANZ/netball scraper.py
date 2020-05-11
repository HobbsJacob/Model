from bs4 import BeautifulSoup
import requests


urlList = []

page = requests.get("http://anzpremiership.co.nz/fixtures-and-results/seasons?season=2017&round=&sdate=&edate=")

soup = BeautifulSoup(page.content, "html.parser")




for tag in soup.find_all("a", text="Match Centre"):
    urlList.append(tag.get("href"))


page = requests.get("http://anzpremiership.co.nz/fixtures-and-results/seasons?season=2018&round=&sdate=&edate=")

soup = BeautifulSoup(page.content, "html.parser")




for tag in soup.find_all("a", text="Match Centre"):
    urlList.append(tag.get("href"))



page = requests.get("http://anzpremiership.co.nz/fixtures-and-results/seasons?season=2019&round=&sdate=&edate=")

soup = BeautifulSoup(page.content, "html.parser")




for tag in soup.find_all("a", text="Match Centre"):
    urlList.append(tag.get("href"))





for url in urlList:
    print(url)

    split = url.split("&matchid=")
    matchId = split[1]
    competitionId = split[0].split("competitionid=")[1]
    
    with open("json/" + matchId + ".json", "wb") as file:
        page = requests.get("https://mc.championdata.com/data/" + competitionId + "/" + matchId + ".json")
        file.write(page.text.encode('unicode'))






