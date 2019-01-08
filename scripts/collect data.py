# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 15:21:11 2018

@author: ning
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
import utils
import os
from time import sleep
from tqdm import tqdm

saving_dir = '../tables'
if not os.path.exists(saving_dir):
    os.mkdir(saving_dir)

urls = ['http://cba.sports.sina.com.cn/cba/schedule/all/?qleagueid={}&qmonth=&qteamid='.format(kk) for kk in [180,189,198]]
for url in urls:
    page = urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    
    table = soup.find_all('table')[1]
    column_names = 'round Date Home_team scores Away_team report stats pic location TV'.split(' ')
    temp = {ii:[] for ii in range(10)}
    links = []
    for i_row,row in enumerate(table.find_all('tr')):
        for i_col,column in enumerate(row.find_all('td')):
            info = (column.get_text()
                          .replace('\n','')
                          .replace('\t','')
                          .replace('\xa0',' ')
                         )
            link = column.find_all('a',href=True)
            if len(link) > 0:
                if ('统计' in link[0]):
                    links.append(link[0]['href'])
            if len(info) > 50:
                info = info[28] + info[29]
            else:
                try:
                    s1,s2 = re.findall('\d+',info)
                    info = '{}:{}'.format(s1,s2)
                except:
                    pass
            temp[i_col].append(info)
    
    summary = pd.DataFrame(temp)
    summary.columns = column_names
    summary['links'] = links
    
    
    for ii,row in tqdm(summary.iterrows()):
        stats_link = row['links']
        page = urlopen(stats_link)
        soup = BeautifulSoup(page,'html.parser')
        
        home_team = soup.find_all('table')[0]
        away_team = soup.find_all('table')[-2]
        
        home_stats = utils.parse_table_stats(home_team)
        home_stats['Fast_break'] = home_stats['Fast_break'].apply(utils.strange_things)
        home_stats['Scores'] = home_stats['Scores'].apply(utils.strange_things)
        away_stats = utils.parse_table_stats(away_team)
        
        home_stats['team'] = row['Home_team']
        away_stats['team'] = row['Away_team']
        
        home_stats['date'] = row['Date'].split(' ')[0]
        away_stats['date'] = row['Date'].split(' ')[0]
        stats_table = pd.concat([home_stats,away_stats])
        saving_name = '{} vs {} ({}).csv'.format(row['Home_team'],
                                                 row['Away_team'],
                                                 row['Date'].split(' ')[0])
        stats_table.to_csv(os.path.join(saving_dir,saving_name),
                           index = False,
                           encoding = 'utf_8_sig')
        sleep(5)













