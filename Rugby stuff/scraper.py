from selenium import webdriver
import time


starting = 355011
ending = 355012

driver = webdriver.Chrome()

while starting <= ending:
    

    driver.get("https://super.rugby/superrugby/match-centre/?season=2020&competition=355&match=" + str(starting))
    time.sleep(1)
    driver.get("https://omo.akamai.opta.net/auth/?feed_type=ru7&game_id=" + str(starting) + "&user=OW2017&psw=dXWg5gVZ&jsoncallback=ru7_" + str(starting))

    try:
        

        if len(driver.find_element_by_tag_name("pre").text) > 2000:
            with open("C:\\Users\\Jacob\\Desktop\\datas\\" + str(starting) + ".json", "w") as file:
                file.write(driver.find_element_by_tag_name("pre").text)

    except:
        print("it rage quit")

    starting += 1
