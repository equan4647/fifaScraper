import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
url_card = "https://fifarenderz.com/21/players"
base_url = "https://fifarenderz.com"

###############Code for writing page to file

# htfile=open("myhtm.txt","w",encoding='utf-8')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url_card)
#time.sleep(10)
html = driver.execute_script('return document.documentElement.outerHTML')
# htfile.write(html)
#
##########################################

# f = open("myhtm.txt", "r")

# html = f.read()
main_web_soup = BeautifulSoup(html, 'html.parser')


players = main_web_soup.findAll("a", {"class": "flex justify-start items-center player-list-item"})


driver.close()

for player in players:
    driver = webdriver.Chrome(chrome_options=chrome_options)
    url_player = base_url + player['href']
    driver.get(url_player)  
    p_html = driver.execute_script('return document.documentElement.outerHTML')
    web_soup = BeautifulSoup(p_html, 'html.parser')
    driver.close()
    

    ### SOUP data


    name =  ( web_soup.findAll("div", {"class": "vs-list--title"}))[4].string
    attributes = web_soup.findAll("div", {"class": "vs-list--subtitle"})
    stat_bundle = web_soup.findAll("span", {"class": "stat"})
    rating = web_soup.find("span", {"class": "rating"}).string
    position = web_soup.find("span", {"class": "position"}).string
    card_name = web_soup.find("span", {"class": "name"}).string
    image = web_soup.find("img", {"class": "player-img"})['src']
    checm_bundle = web_soup.findAll("p", {"class": "w-1/3"})




    #### EXtraction


    #Chem

    ch_club = checm_bundle[5].getText().split()[0]
    ch_league = checm_bundle[8].getText().split()[0]
    ch_nation = checm_bundle[11].getText().split()[0]
    ch_program = checm_bundle[13].getText().split()[0]
    ch_given = checm_bundle[16].getText().split()[0]
    ch_taken = checm_bundle[19].getText().split()[0]

    #stats

    pace_ovrl = stat_bundle[0].string
    acceleration = stat_bundle[1].string
    sprint_speed = stat_bundle[2].string
    shootig_ovrl = stat_bundle[3].string
    positioning = stat_bundle[4].string
    finishing = stat_bundle[5].string
    shot_power = stat_bundle[6].string
    longShot = stat_bundle[7].string
    volleys = stat_bundle[8].string
    panelties = stat_bundle[9].string
    passing_ovrl = stat_bundle[10].string
    vision = stat_bundle[11].string
    crossing = stat_bundle[12].string
    freekick = stat_bundle[13].string
    shortpass = stat_bundle[14].string
    longpass = stat_bundle[15].string
    curve = stat_bundle[16].string
    agility_overall = stat_bundle[17].string
    agility = stat_bundle[18].string
    balance = stat_bundle[19].string
    reaction = stat_bundle[20].string
    ballctrl = stat_bundle[21].string
    dribling = stat_bundle[22].string
    def_over = stat_bundle[23].string
    intersep = stat_bundle[24].string
    header = stat_bundle[25].string
    marking = stat_bundle[26].string
    stand_tackle = stat_bundle[27].string
    slide_tackle = stat_bundle[28].string
    physical = stat_bundle[29].string
    jumping = stat_bundle[30].string
    strength = stat_bundle[31].string
    agresion = stat_bundle[32].string

    #info

    skill = attributes[0].string
    skill2 = attributes[1].string
    celeb = attributes[2].string
    traits = attributes[3].string
    skillboost = attributes[4].string
    club = attributes[5].string
    nation = attributes[6].string
    foot = attributes[7].string
    wfrating = attributes[8].string
    height = attributes[9].string
    weight = attributes[10].string
    attdef = attributes[11].string
    source = attributes[12].string


    print("-----------------------")
    print(name)
    print(position)
    print(club)
    print("-----------------------")





########TODO
# work on fife
# get GK skills
# card data , image , backgroud stuff