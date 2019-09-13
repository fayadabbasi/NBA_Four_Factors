import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time

import pickle

season = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
# this probably needs to be broken down to manageable size - maybe as a dictionary for seasons
months = ['october','november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']



pages = []
just_game_tag = []
for year in [2018,2019]:
    for month in ['october','november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']:
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'.format(year,month)
        page = requests.get(url)
        soup = BeautifulSoup(page.text)
        for tag in soup.find_all("a", string="Box Score"):
            pages.append('https://www.basketball-reference.com/boxscores/{}'.format(tag['href']))
            just_game_tag.append(tag['href'][11:-5])
        time.sleep(15)
        

with open('tags.pkl', 'wb') as fp:
    pickle.dump(just_game_tag, fp)

with open ('tags.pkl', 'rb') as fp:
    new_lst = pickle.load(fp)