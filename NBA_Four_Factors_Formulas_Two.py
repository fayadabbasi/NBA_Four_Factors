import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
import numpy as np

def web_scrape(year,month,day,team):    
    web_template = (f'https://www.basketball-reference.com/boxscores/{year}{month}{day}0{team}.html')
    data = requests.get(web_template)
    soup = BeautifulSoup(data.text, 'html.parser')
    headers_four_factors = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    rows = soup.findAll('tr')[2:]
    player_stats1 = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    player_names1 = [[td.getText() for td in rows[i].findAll('th')] for i in range(len(rows))]
    stats = pd.DataFrame(player_stats1, columns = headers_four_factors[1:])
    player = pd.DataFrame(player_names1)
    player = player[0][:66]
    stats['Player'] = player
    return stats

def team_summary(year,month,day,team):    
    web_template = (f'https://www.basketball-reference.com/boxscores/{year}{month}{day}0{team}.html')
    data = requests.get(web_template)
    soup = BeautifulSoup(data.text, 'html.parser')
    rows2 = soup.findAll(class_='scorebox')
    overall_teams = [strong.getText() for strong in rows2[0].findAll('strong')]
    overall_teams = [items.strip('\n') for items in overall_teams]
    overall_score = [scores.getText() for scores in rows2[0].findAll(class_='scores')]
    overall_score = [items.strip('\n') for items in overall_score]
    
    def date_adjustment():
        overall_date = [dates.getText() for dates in rows2[0].findAll(class_='scorebox_meta')]
        overall_date = [items.strip('\n') for items in overall_date]
        overall_date_2 = [items.split(',') for items in overall_date]
        output_list = []
        output_list.append(overall_date_2[0][0])
        output_list.append(overall_date_2[0][1])
        output_list.append(overall_date_2[0][2][:5].strip(' '))
        
        return output_list
    
    date_list = [' '.join(date_adjustment())] * 2
    teams_scores = pd.DataFrame(overall_teams, columns=['Team_Name'])
    teams_scores['Score'] = overall_score
    teams_scores['Date'] = date_list
    return teams_scores

def four_factors_output(year,month,day,team):
    stats = web_scrape(year,month,day,team)
    teams_scores = team_summary(year,month,day,team)
    test = stats[['Player','MP','FG', 'FGA', '3P', 'FT', 'ORB', 'TOV', 'FTA', 'DRB', 'PTS']]    
    test_list = ['FG', 'FGA', '3P', 'FT', 'ORB', 'TOV', 'FTA', 'DRB']
    test = test.dropna()
    for items in test_list:
        test[items] = pd.to_numeric(test[items], errors='coerce').fillna(0).astype(int)
    
    test['Player'][test['PTS']==teams_scores['Score'].iloc[0]] = teams_scores['Team_Name'].iloc[0]
    test['Player'][test['PTS']==teams_scores['Score'].iloc[1]] = teams_scores['Team_Name'].iloc[1]
    test['Date'] = teams_scores['Date'].iloc[0]
    
    test['eFG'] = (test['FG'] + 0.5* test['3P']) / test['FGA']
    test['TOV_per'] = test['TOV'] / (test['FGA'] + 0.44 * test['FTA'] + test['TOV'])
    test['ORB_per'] = test['ORB'] / (test['ORB'] + test['DRB'])
    test['FTr'] = test['FT'] / test['FGA']
    four_factors_dataframe = test[['Player', 'eFG', 'TOV_per', 'ORB_per', 'FTr', 'Date']]
    
    uniq_id = str(year)+str(month)+str(day)+team
    append_data = test.loc[[14,48],:]
    append_data['id_t'] = uniq_id
    append_data['loc'] = team
    return append_data

