import psycopg2 as pg2
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
import pickle
import time

engine = create_engine('postgresql+psycopg2://postgres:docker@localhost:5432/nbafourfactor')

with open ('tags.pkl', 'rb') as fp:
    new_lst = pickle.load(fp)

len(new_lst)

import NBA_Four_Factors_Formulas_Two as nba

x = len(new_lst)

for y in range(x):
    df = nba.four_factors_output(new_lst[y])
    df.to_sql('nbafourfactorfour',engine, if_exists='append',index=False)
    time.sleep(15)