#!/usr/bin/env python
# coding: utf-8

# In[214]:


import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
import numpy as np


# In[215]:


year, month, day, team = 2018, 10, 19, 'ORL'
web_template = (f'https://www.basketball-reference.com/boxscores/{year}{month}{day}0{team}.html')


# In[216]:


def web_scrape():
    year, month, day, team = 2018, 10, 19, 'ORL'    
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


# In[217]:


def team_summary():
    year, month, day, team = 2018, 10, 19, 'ORL'    
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
    


# In[218]:


web_template


# In[219]:


test = web_scrape()


# In[220]:


test[:15]


# In[227]:


team_summary()


# In[228]:


teams_scores = team_summary()


# In[229]:


def four_factors_output():
    
    
    four_factors_dataframe_test = stats[['Player','MP','FG', 'FGA', '3P', 'FT', 'ORB', 'TOV', 'FTA', 'DRB']]    
    test_list = ['FG', 'FGA', '3P', 'FT', 'ORB', 'TOV', 'FTA', 'DRB']
    four_factors_dataframe_test = four_factors_dataframe_test.dropna()
    for items in test_list:
        four_factors_dataframe_test[items] = pd.to_numeric(four_factors_dataframe_test[items], errors='coerce').fillna(0).astype(int)
    
    if (four_factors_dataframe_test['FG'].iloc[13] * 2) + four_factors_dataframe_test['3P'].iloc[13] + four_factors_dataframe_test['FT'].iloc[13] == int(teams_scores['Score'].iloc[0]):
        four_factors_dataframe_test['Player'].iloc[13] = teams_scores['Team_Name'].iloc[0]
        four_factors_dataframe_test['Player'].iloc[-1] = teams_scores['Team_Name'].iloc[1]
        four_factors_dataframe_test['Date'] = teams_scores['Date'].iloc[0]
        four_factors_dataframe_test['Date'] = teams_scores['Date'].iloc[0]
    else:
        four_factors_dataframe_test['Player'].iloc[13] = teams_scores['Team_Name'].iloc[1]
        four_factors_dataframe_test['Player'].iloc[-1] = teams_scores['Team_Name'].iloc[0]
        four_factors_dataframe_test['Date'] = teams_scores['Date'].iloc[0]
        four_factors_dataframe_test['Date'] = teams_scores['Date'].iloc[0]
    
    
    four_factors_dataframe_test['eFG'] = (four_factors_dataframe_test['FG'] + 0.5* four_factors_dataframe_test['3P']) / four_factors_dataframe_test['FGA']
    four_factors_dataframe_test['TOV%'] = four_factors_dataframe_test['TOV'] / (four_factors_dataframe_test['FGA'] + 0.44 * four_factors_dataframe_test['FTA'] + four_factors_dataframe_test['TOV'])
    four_factors_dataframe_test['ORB%'] = four_factors_dataframe_test['ORB'] / (four_factors_dataframe_test['ORB'] + four_factors_dataframe_test['DRB'])
    four_factors_dataframe_test['FTr'] = four_factors_dataframe_test['FT'] / four_factors_dataframe_test['FGA']
    four_factors_dataframe = four_factors_dataframe_test[['Player', 'eFG', 'TOV%', 'ORB%', 'FTr', 'Date']]
    
    year, month, day, team = 2018, 10, 19, 'ORL'
    uniq_id = str(year)+str(month)+str(day)+team
    append_data = four_factors_dataframe_test.loc[[14,48],:]
    append_data['id_t'] = uniq_id
    return append_data


# In[230]:


stats = test


# In[231]:


four_factors_dataframe_test = four_factors_output()


# In[232]:


four_factors_dataframe_test


# In[ ]:





# In[ ]:





# In[ ]:




