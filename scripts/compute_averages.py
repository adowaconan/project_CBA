# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 12:09:55 2018

@author: ning
"""

import pandas as pd
from glob import glob
import os

def get_averages():
    working_dir = '..\\tables'
    working_data = glob(os.path.join(working_dir,'*.csv'))
    df = pd.concat([pd.read_csv(f,engine='python',encoding = 'utf_8_sig') for f in working_data])
    column_names = ['Player', 'NO', 'Minutes', 'Starter', '2Pt', '3Pt', 'FT', 'OffReb',
           'DefReb', 'Ass', 'Foul', 'Steal', 'TO', 'Block', 'Dunk', 'Fouled',
           'Fast_break', 'Scores', 'team', 'date']
    df.columns = column_names
    
    columns = ['2Pt','3Pt','FT']
    for name in columns:
        df['{}_made'.format(name)] = df[name].apply(lambda x:int(x.split('-')[0]))
        df['{}_attempt'.format(name)] = df[name].apply(lambda x:int(x.split('-')[1]))

    return ([df['{}_made'.format(name)].sum() / float(df['{}_attempt'.format(name)].sum()) for name in columns],
                df,
                )






















