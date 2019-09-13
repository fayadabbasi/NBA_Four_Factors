# NBA Four Factors

## Thesis

As a fan of NBA basketball, I have been fascinated by the impact analytics has had on the game over the past 10-15 years. Following the insight that 3pts > 2pts, teams started to significantly emphasize shooting 3pt shots, largely at the expense of the mid-range 2pt shot. There was a lot of research done into what key factors led to wins vs losses. The thesis I wanted to explore was do those factors look similar for home teams versus away teams and if not, which ones show variance. My bias was that road teams would not be as energetic as home teams and things like rebounding and turnovers could be an advantage for home teams. So I looked at the four factors and tested each to see if those two samples are statistically different.  

## Background

Dean Oliver, considered one of the innovators and early practicioner of applying statistics to basketball, has posited a way of looking at what drives wins in an NBA game, known as the Four Factor. His research shows there are Four Factors that drive wins for a team, in order of importance:

1. **Effective FG%**: effective field goal percent is an adjustment to the overall field goal statistic. The formula is (FGM + 0.5 * 3PFGM) / FGA. The more shots you make, the better your chances of winning and a 3 point made is 50% more valuable than 2 points. Dean has estimated that this factor weighting is about 40%.

2. **Turnover %**: Turnover percent is the rate at which the ball is turned over. A turnover results in zero attempts to score so you are not giving yourself a chance to add points when you turn the ball over. It is calculated as TOV / (FGA + 0.44 * FTA + TOV). TOV % is estimated at a weighting of 25%.

3. **Offensive Rebound %**: Offensive rebounds give you additional opportunities and conversely limit the other team from future opportunities. ORB is calculated as ORB / (ORB + DRB). The weighting estimated is 20%.

4. **FT Rate**: Finally, free throw rate is the amount of free throws a team had in a game. This is a metric that is not captured in field goals but is definitely a contributor to points scored. It is calculated as FT / FGA and its estimated weighting is 15%.

In this study, I will not analyze how effective these four factors are to determine a win or loss. The literature suggests they have a very strong predictive capability and we can return to how strong in a future analysis. 

***

# What am I testing for?

I am looking to determine the following: *Do NBA teams have a home court advantage?* I will analyze data from the 2017-2018 season, including playoffs. 
Looking at home teams and away teams, I will have two samples of:

> Regular Season: 82 games per team * 30 teams / 2 teams play at a time ==> 1230 

> Playoffs: will vary 

I will perform 4 t-tests, one for each of the four factors. My **null hypothesis** for each test is there is no difference between home games and away games as it relates to the four factors. 
My **alternative hypothesis** is that there is a difference. I am using a two sided t-test with two degrees of freedom. 

***

# Techniques used

I first scraped data by team for the 2017-2018 season from www.basketball-reference.com. I used pickle to create a series of unique identifiers for each game box score URL. I then set up a script to run a .py file with three functions. 

1. The first function scraped the specified page and got team box score data. This includes all the box score data for each player and team summaries. Note that I had to create two lists, one for team statistics and a separate one for the player or team name, and then combine them. My output was a pandas dataframe. Below is a sample of the code from the first function. 

```python
web_template = (f'https://www.basketball-reference.com/boxscores/{year}{month}{day}0{team}.html')
data = requests.get(web_template)
soup = BeautifulSoup(data.text, 'html.parser')
# scrape the site
    
    
headers_four_factors = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
rows = soup.findAll('tr')[2:]
player_stats1 = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
player_names1 = [[td.getText() for td in rows[i].findAll('th')] for i in range(len(rows))]
# run some list comprehensions to identify the headers for the table, the player statistics and separately 
# the player name since that is not included in player statistics
    
stats = pd.DataFrame(player_stats1, columns = headers_four_factors[1:])
player = pd.DataFrame(player_names1)
player = player[0][:66]
stats['Player'] = player
# create a statistics dataframe and a player name dataframe and then append the player name to the stats
# return the assembled dataframe
```

2. The second function scraped a different part of the page with a summary box score. This included the teams that played, the location the game was played and time, and the final score. The output was a pandas dataframe. 

```python
web_template = (f'https://www.basketball-reference.com/boxscores/{year}{month}{day}0{team}.html'
data = requests.get(web_template)
soup = BeautifulSoup(data.text, 'html.parser')
rows2 = soup.findAll(class_='scorebox')
overall_teams = [strong.getText() for strong in rows2[0].findAll('strong')]
overall_teams = [items.strip('\n') for items in overall_teams]
# creates dataframe with team name information, including striping unnecessary data

overall_score = [scores.getText() for scores in rows2[0].findAll(class_='scores')]
overall_score = [items.strip('\n') for items in overall_score]
# creates dataframe with summary score information, including striping unnecessary data


def date_adjustment():
    overall_date = [dates.getText() for dates in rows2[0].findAll(class_='scorebox_meta')]
    overall_date = [items.strip('\n') for items in overall_date]
    overall_date_2 = [items.split(',') for items in overall_date]
    
    output_list = []
    output_list.append(overall_date_2[0][0])
    output_list.append(overall_date_2[0][1])
    output_list.append(overall_date_2[0][2][:5].strip(' '))
    # this function gets me the appropriate date information

    return output_list
    
date_list = [' '.join(date_adjustment())] * 2
teams_scores = pd.DataFrame(overall_teams, columns=['Team_Name'])
teams_scores['Score'] = overall_score
teams_scores['Date'] = date_list
# this creates the final dataframe to output from the second function
```


3. My third function took the above two dataframes and combined it into the information used for my analysis. Specifically, I needed to take team name from the second dataframe and combine it with the summary statistics from the first dataframe. The output was a pandas dataframe. 

```python
stats = web_scrape(inputlist)
teams_scores = team_summary(inputlist)
test = stats[['Player','MP','FG', 'FGA', '3P', 'FT', 'ORB', 'TOV', 'FTA', 'DRB', 'PTS']]    
test_list = ['FG', 'FGA', '3P', 'FT', 'ORB', 'TOV', 'FTA', 'DRB']
# creating the fields for the output dataframe and running the above two functions to get the respective information

test = test.dropna()
for items in test_list:
    test[items] = pd.to_numeric(test[items], errors='coerce').fillna(0).astype(int)
# by eliminating the na and converting to numeric, I can then perform some basic math on the columns


test['Player'][test['PTS']==teams_scores['Score'].iloc[0]] = teams_scores['Team_Name'].iloc[0]
test['Player'][test['PTS']==teams_scores['Score'].iloc[1]] = teams_scores['Team_Name'].iloc[1]
test['Date'] = teams_scores['Date'].iloc[0]
# since the dataframe does not actually have the team names in, identify the team name by the score from the team_summary function


test['eFG'] = (test['FG'] + 0.5* test['3P']) / test['FGA']
test['TOV_per'] = test['TOV'] / (test['FGA'] + 0.44 * test['FTA'] + test['TOV'])
test['ORB_per'] = test['ORB'] / (test['ORB'] + test['DRB'])
test['FTr'] = test['FT'] / test['FGA']
four_factors_dataframe = test[['Player', 'eFG', 'TOV_per', 'ORB_per', 'FTr', 'Date']]
# this is the four factors for the dataframe I am interested in
    
uniq_id = str(year)+str(month)+str(day)+team
append_data = test[test['Player']==teams_scores['Team_Name'][0]]
append_data = append_data.append(test[test['Player']==teams_scores['Team_Name'][1]])
append_data['id_t'] = uniq_id
append_data['loc'] = team
# some additional fields I have added to my dataframe for output

```


I took the output of third dataframe and fed that into a PostGresSQL database in a Docker container. I ran the script on my local machine with an approximate run time of 5 hours, as I found I needed to add a sleep time of 15 seconds between scrapes to avoid getting timed out. 

```python
engine = create_engine('postgresql+psycopg2://postgres:docker@localhost:5432/nbafourfactor')

with open ('tags.pkl', 'rb') as fp:
    new_lst = pickle.load(fp)
# this is the list of unique URLs

import NBA_Four_Factors_Formulas_Two as nba
# this is the file name of my functions above

x = len(new_lst)
# this is the total number of entries from the pickle list of unique urls

for y in range(x):
    df = nba.four_factors_output(new_lst[y])
    df.to_sql('nbafourfactorfour',engine, if_exists='append',index=False)
    time.sleep(15)
```


After the 2017-2018 data was entered, I had a total of 2,644 rows of data to analyze. I then pulled the data into two pandas dataframe, one for home games and another for away games. I plotted histograms of the calculated four factors for home and away games. 

# Findings

I was surprised to see how my normal distributions appeared, well normal. The Free Throw Rate distributions exhibited a slight right skew but otherwise the distributions appeared textbook. I then performed a t-test for each factor. As stated in the thesis, my bias was that a larger variance between home and away teams existed for hustle factors, such as rebounding and turnovers. What the data showed was the opposite. Turnover percent and offensive rebounding percent had p-values of xxx and xxx, respectively. So despite the travel, road teams apparently get plenty of rest and are ready to play at game time. 

Perhaps equally fascinating was that the effective field goal rate *did* show a materially relevant p-value. Free throw rate p-value was 0.028, resulting in our rejecting our null hypothesis for it as well. The home team apparently does have more comfort shooting in their own arena as indicated by the field goal rate and perhaps the home team does get more free throw attempts (perhaps driven by some favorable referee calls). 

### Effective Field Goal Percentage

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/blob/master/efg_histograms.png "effective FG% for home in blue and away in orange")

```
The mean effective FG% for home games is 0.528 and the standard deviation is 0.0646
The mean effective FG% for away games is 0.516 and the standard deviation is 0.06459
Performing a t-test on the two samples, the t-statistic is 5.0 and the p-value is 6.044e-07

```

### Free Throw Rate

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/blob/master/ftr_histograms.png "free throw rate for home in blue and away in orange")

```
The mean Free Throw Rate for home games is 0.201 and the standard deviation is 0.07566
The mean Free Throw Rate for away games is 0.195 and the standard deviation is 0.07421
Performing a t-test on the two samples, the t-statistic is 2.2 and the p-value is 0.02818

```

### Offensive Rebound percent

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/blob/master/orb_histograms.png "offensive rebound percent for home in blue and away in orange")

```
The mean Offensive Rebound Percent for home games is 0.222 and the standard deviation is 0.07029
The mean Offensive Rebound Percent for away games is 0.223 and the standard deviation is 0.07142
Performing a t-test on the two samples, the t-statistic is -0.432 and the p-value is 0.6656
```


### Turnover percent

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/blob/master/tov_histograms.png "turnover percent for home in blue and away in orange")

```
The mean Turnover Percent for home games is 0.124 and the standard deviation is 0.03244
The mean Turnover Percent for away games is 0.126 and the standard deviation is 0.03385
Performing a t-test on the two samples, the t-statistic is -1.13 and the p-value is 0.2579
```

### Team leaders 

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/tree/master/tables_nba/eFG_percent_team_lead_20172018.png "team leaders for effective field goals")

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/tree/master/tables_nba/ftr_team_lead_20172018.png "team leaders for free throw rate goals")

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/tree/master/tables_nba/orb_team_lead_20172018.png "team leaders for offensive rebound percent goals")

![alt text](https://github.com/fayadabbasi/NBA_Four_Factors/tree/master/tables_nba/tov_team_lead_20172018.png "team leaders for turnover rate goals")

# Future Analysis

Additional tests to perform could include: 

> what is the impact of a multi-day road trip? More variance or the same results?

> how do these factors evolve over the past 10 years of NBA games? 15 years?

> how much do each of the four factors contribute to determining the outcome of a game? How has that evolved over the past 10 years? 15 years?

> which teams lead in each of the four factors? which teams constitute the bottom of the league for those factors?

> visualize how shot distribution has resulted in hollowing out of the mid-range jump shot in the past 15 years. 

# Technologies demonstrated

 - Beautiful Soup
 - Pandas DataFrames
 - SQL Alchemy
 - PostgresSQL 
 - Matplotlib
 - Seaborn

# References

Thanks to Joseph Gartner, Dan Rupp, Brent Goldberg, Keatra Nesbitt from Galvanize for assistance in this process. Thanks to the many bloggers that have written about the Four Factors, including Square2020, Savvas Tjortjoglou, and others. Thanks to Basketball Reference for the data.  
