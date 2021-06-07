import pandas as pd
import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup

def espn_gamelog_to_excel(url):

    page = requests.get(url)

    raw_data = BeautifulSoup(page.content, 'html.parser')

    stats = raw_data.find_all('td')
    playername = raw_data.find_all('h1')
    year_raw = raw_data.find_all('h2')

    for c, i in enumerate(playername):
        playername[c] = i.get_text()

    for c, i in enumerate(year_raw):
        year_raw[c] = i.get_text()

    for c, i in enumerate(stats):
        stats[c] = i.get_text()

    year = year_raw[0]
    name = playername[0]

    sorted_stats = []
    counter = 0

    dow = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for count, i in enumerate(stats):
        for a in dow:
            if a in i:
                sorted_stats.append(stats[count:count + 17])

    col = ["Date", "Opponent", "Result", "Minutes", "Field Goals", "Field Goal Percentage", "3 Pointers", "3 Point Percentage", "Free Throws", "Free Throw Percentage", "Rebounds", "Assists", "Blocks", "Steals", "Personal Fouls", "Turnovers", "Points"]

    df = pd.DataFrame(sorted_stats, columns = col)

    #df.to_excel(name + "_" + year + ".xlsx")

    return [df, name]

def fgp_h_vs_fgp_a(df):
    home_games = []
    away_games = []

    for c, i in df[0].iterrows():
        if "@" in i["Opponent"]:
            away_games.append(float(i["Field Goal Percentage"]))
        else:
            home_games.append(float(i["Field Goal Percentage"]))

    home_fg = 0
    away_fg = 0

    for i in home_games:
        home_fg += i

    for i in away_games:
        away_fg += i

    home_fgp = home_fg / len(home_games)
    away_fgp = away_fg / len(away_games)

    return(df[1], "FG% home vs away " "home: ", round(home_fgp, 2), "%" , "away: ", round(away_fgp, 2))

pprint(fgp_h_vs_fgp_a(espn_gamelog_to_excel("https://www.espn.com/nba/player/gamelog/_/id/3037789/bogdan-bogdanovic")))
pprint(fgp_h_vs_fgp_a(espn_gamelog_to_excel("https://www.espn.com/nba/player/gamelog/_/id/4066372/kevin-huerter")))
pprint(fgp_h_vs_fgp_a(espn_gamelog_to_excel("https://www.espn.com/nba/player/gamelog/_/id/4065732/deandre-hunter")))
pprint(fgp_h_vs_fgp_a(espn_gamelog_to_excel("https://www.espn.com/nba/player/gamelog/_/id/3428/danilo-gallinari")))


