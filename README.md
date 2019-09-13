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

1. The first function scraped the specified page and got team box score data. This includes all the box score data for each player and team summaries. Note that I had to create two lists, one for team statistics and a separate one for the player or team name, and then combine them. My output was a pandas dataframe. 

2. The second function scraped a different part of the page with a summary box score. This included the teams that played, the location the game was played and time, and the final score. The output was a pandas dataframe. 

3. My third function took the above two dataframes and combined it into the information used for my analysis. Specifically, I needed to take team name from the second dataframe and combine it with the summary statistics from the first dataframe. The output was a pandas dataframe. 

I took the output of third dataframe and fed that into a PostGresSQL database in a Docker container. I ran the script on my local machine with an approximate run time of 5 hours, as I found I needed to add a sleep time of 15 seconds between scrapes to avoid getting timed out. 

After the 2017-2018 data was entered, I had a total of 2,644 rows of data to analyze. I then pulled the data into two pandas dataframe, one for home games and another for away games. I plotted histograms of the calculated four factors for home and away games. 

# Findings

I was surprised to see how my normal distributions appeared, well normal. The Free Throw Rate distributions exhibited a slight right skew but otherwise the distributions appeared textbook. I then performed a t-test for each factor. As stated in the thesis, my bias was that a larger variance between home and away teams existed for hustle factors, such as rebounding and turnovers. What the data showed was the opposite. Turnover percent and offensive rebounding percent had p-values of xxx and xxx, respectively. So despite the travel, road teams apparently get plenty of rest and are ready to play at game time. 

Perhaps equally fascinating was that the effective field goal rate *did* show a materially relevant p-value. Free throw rate p-value was 0.028, resulting in our rejecting our null hypothesis for it as well. The home team apparently does have more comfort shooting in their own arena as indicated by the field goal rate and perhaps the home team does get more free throw attempts (perhaps driven by some favorable referee calls). 


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








We will explore several things in this project. First, how much variance do these four factors play per game and are there trends in the mix over the past several years of the NBA? With the mix of shots increasing towards 3 PTs, it would seem that eFG% has increased as a factor. Also, what is the standard deviation of each factor? It would seem that hustle factors such as turnover % and rebounds could have a wider standard deviation than the other factors.

One factor to take into consideration is what is a team. Given free agency and trades, the composition of a team varies year to year as well as within the season. So identifying what the composition of a team is based on the total 240 minutes played per game is important to determine how that specific team's four factors vary.

Next, we will look at the impact of travel. Travel can take a lot out of players and between turnovers and offensive rebounds, which are largely "hustle" factors, how does that impact a team. We will look at the impact on the first game of a road trip, second, third, and fourth. It will be interesting to see if the "team" changes as the length of a road trip increases or if the hustle variables exhibit more variance than normalized variance.

There are some bonus elements that could be included: how does shot selection vary as length of time on the road changes - do teams tend to shoot more 3's while on the road than home or increase the number of 3's as the length of the road trip increases? How does weather play a factor - on flight delay situations, is hustle impacted?

First step is to build a web scraper that gets the data from the website into a manageable format, testing out a sample into a pandas dataframe
Goal for today is to get my web scrape working and get through a good % of the total download I am looking to get through. I believe I have identified all the key factors I am looking to download and last night I got my first dataframe in pandas from an initial one game scrape of data.