import pandas as pd
import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup

def espn_gamelog_to_excel(url, player, year):

    page = requests.get(url)

    raw_data = BeautifulSoup(page.content, 'html.parser')

    stats = raw_data.find_all('td')

    for c, i in enumerate(stats):
        stats[c] = i.get_text()

    sorted_stats = []
    counter = 0

    dow = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for count, i in enumerate(stats):
        for a in dow:
            if a in i:
                sorted_stats.append(stats[count:count + 17])

    col = ["Date", "Opponent", "Result", "Minutes", "Field Goals", "Field Goal Percentage", "3 Pointers", "3 Point Percentage", "Free Throws", "Free Throw Percentage", "Rebounds", "Assists", "Blocks", "Steals", "Personal Fouls", "Turnovers", "Points"]

    df = pd.DataFrame(sorted_stats, columns = col)

    df.to_excel(player + "_" + year + ".xlsx")

espn_gamelog_to_excel("https://www.espn.com/nba/player/gamelog/_/id/4277905/trae-young", "trae-young", "2020-21")
