# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 16:37:49 2018

@author: ning
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd

def parse_table_stats(team):
    column_names = 'player 	NO 	Minutes 	Starter 	2Pt 	3Pt 	FT 	OffReb 	DefReb 	Ass 	Foul 	Steal 	TO 	Block 	Dunk 	Fouled 	Fast_break 	Scores'.split(' 	')
    temp = {ii:[] for ii in range(len(column_names))}
    for i_row,row in enumerate(team.find_all('tr')[:-1]):
        for i_col,column in enumerate(row.find_all('td')):
            info = (column.get_text()
                          .replace('\n','')
                          .replace('\t','')
                          .replace('\xa0',' ')
                          .replace(' ','')
                         )
            if (i_col == 4) or (i_col == 5) or (i_col == 6):
                a,b,c = re.findall('\d+',info)
                info = '{}-{}'.format(a,b)
            temp[i_col].append(info)
    stats_table = pd.DataFrame(temp)
    stats_table.columns = column_names
    
    return stats_table

def get_home_away_stats(stats_link):
    page = urlopen(stats_link)
    soup = BeautifulSoup(page,'html.parser')
    
    home_team = soup.find_all('table')[-3]
    away_team = soup.find_all('table')[-2]
    
    home_stats = parse_table_stats(home_team)
    away_stats = parse_table_stats(away_team)
    
    return home_stats,away_stats

def strange_things(x):
    temp = re.findall('\d+',x)
    if len(temp) > 1:
        a,b = temp
        temp = '{}/{}'.format(a,b)
    else:
        temp = temp[0]
    return temp

