# NBA Four Factors

## Thesis

Dean Oliver, considered one of the innovators and early practicioner of applying statistics to basketball, has posited a way of looking at what drives wins in an NBA game, known as the Four Factor. His research shows there are Four Factors that drive wins for a team, in order of importance:

1 **Effective FG%**: eFG% is an adjusted FG% view. The formula is (FGM + 0.5 * 3PFG) / FGA. The more shots you make, the better your chances of winning. Dean has estimated that this factor weighting is about 40%.

2 **Turnover %**: TOV% is the rate at which the ball is turned over. It is calculated as TOV / (FGA + 0.44 * FTA + TOV). TOV % is estimated at a weighting of 25%.

3 **Offensive Rebound %**: Offensive rebounds give you additional opportunities. As stated, they are accounted for as ORB / (ORB + DRB). The weighting estimated is 20%.

4 **FT Rate**: Finally, free throw rate is the amount of free throws a team had in a game. It is calculated as FT / FGA and its estimated weighting is 15%.

***

# What are we testing for?

We are looking to perform a relatively simple analysis: *Do NBA teams have a home court advantage?* We will analyze data from the 2017-2018 season, including playoffs. 
Looking at home teams and away teams, we will have two samples of:

> Regular Season: 82 games per team * 30 teams / 2 teams play at a time ==> 1230 

> Playoffs: will vary 

We will perform 4 t-tests, one for each of the four factors. Our **null hypothesis** for each test is there is no difference between home games and away games as it relates to the four factors. 
Our **alternative hypothesis** is that there is a difference. We are using a two sided test with two degrees of freedom. 

***

# Data used

We first scraped data by team for the 2017-2018 season from www.basketball-reference.com. We used pickle to create a series of unique identifiers for each game box score URL.   





We will explore several things in this project. First, how much variance do these four factors play per game and are there trends in the mix over the past several years of the NBA? With the mix of shots increasing towards 3 PTs, it would seem that eFG% has increased as a factor. Also, what is the standard deviation of each factor? It would seem that hustle factors such as turnover % and rebounds could have a wider standard deviation than the other factors.

One factor to take into consideration is what is a team. Given free agency and trades, the composition of a team varies year to year as well as within the season. So identifying what the composition of a team is based on the total 240 minutes played per game is important to determine how that specific team's four factors vary.

Next, we will look at the impact of travel. Travel can take a lot out of players and between turnovers and offensive rebounds, which are largely "hustle" factors, how does that impact a team. We will look at the impact on the first game of a road trip, second, third, and fourth. It will be interesting to see if the "team" changes as the length of a road trip increases or if the hustle variables exhibit more variance than normalized variance.

There are some bonus elements that could be included: how does shot selection vary as length of time on the road changes - do teams tend to shoot more 3's while on the road than home or increase the number of 3's as the length of the road trip increases? How does weather play a factor - on flight delay situations, is hustle impacted?

First step is to build a web scraper that gets the data from the website into a manageable format, testing out a sample into a pandas dataframe
Goal for today is to get my web scrape working and get through a good % of the total download I am looking to get through. I believe I have identified all the key factors I am looking to download and last night I got my first dataframe in pandas from an initial one game scrape of data.