# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 12:44:59 2018

@author: ning

This script defines 2pt efficiency as the ratio between A and B, where A is the
personal 2pt made = 2 * 2pt percentage
and
B is the game average 2pt made: 2 * 2pt percentage of everyone
Higher than 0 means the player is more efficient than the average of the single game

3pt efficiency is defined as the same while the scoring base is changed to 3 instead
of 2

"""

import pandas as pd
import os
from glob import glob
import seaborn as sns
sns.set_style('whitegrid')
sns.set_context('poster')
from scipy import stats
from matplotlib import pyplot as plt


working_dir = '..\\tables'
figure_dir = '..\\figures'
if not os.path.exists(figure_dir):
    os.mkdir(figure_dir)
working_data = glob(os.path.join(working_dir,'*.csv'))
columns = ['2Pt','3Pt','FT']
temp = []
for ii,f in enumerate(working_data):
    d = pd.read_csv(f,engine='python',encoding = 'utf_8_sig')
    if len(d) > 0:
        d['game_id'] = ii
        for name in columns:
            d['{}_made'.format(name)] = d[name].apply(lambda x:int(x.split('-')[0]))
            d['{}_attempt'.format(name)] = d[name].apply(lambda x:int(x.split('-')[1])) + 1
            percentage = d['{}_made'.format(name)].values / d['{}_attempt'.format(name)].values
            try:
                baseline_score = float(int(name[0]))
            except:
                baseline_score = 1.
            actual = percentage * baseline_score
            expect = d['{}_made'.format(name)].sum() / float(d['{}_attempt'.format(name)].sum()) * baseline_score
            d['{}_eff'.format(name)] = actual - expect
        temp.append(d)
df = pd.concat(temp)

df = df[df['player'] != '未确认'] # take out the rows we don't want
# let's plot the 2pt efficiency against 3pt efficiency for individual player
for player,df_work in df.groupby('player'):
    plt.close('all')
    try:
        g = sns.JointGrid(x = '2Pt_eff',
                          y = '3Pt_eff',
                          data = df_work,
                          height = 10,
                          ratio = 3,)
        g = g.plot_joint(sns.kdeplot,cmap='Blues_d')
        g = g.plot_marginals(sns.kdeplot,shade=True)
        rsquare = lambda a,b:stats.spearmanr(a,b)[0] ** 2
        g = g.annotate(rsquare,
                       template='{stat}= {val:.5f}',
                       stat='$R^2$',
                       loc='upper left',
                       fontsize=12)
        g.set_axis_labels('2Pt efficiency','3Pt efficiency')
        g.fig.axes[0].axhline(0.,linestyle='--',color='black',alpha=0.5)
        g.fig.axes[0].axvline(0.,linestyle='--',color='black',alpha=0.5)
        g.savefig(os.path.join(figure_dir,'rsquared {}.png'.format(player)),
                  bbox_inches = 'tight')

        g = sns.jointplot(x = '2Pt_eff',
                          y = '3Pt_eff',
                          data = df_work,
                          kind = 'kde',
                          height = 10,
                          ratio = 3,
                          stat_func = stats.spearmanr)
        g.set_axis_labels('2Pt efficiency','3Pt efficiency')
        g.fig.axes[0].axhline(0.,linestyle='--',color='black',alpha=0.5)
        g.fig.axes[0].axvline(0.,linestyle='--',color='black',alpha=0.5)
        g.savefig(os.path.join(figure_dir,'correlation {}.png'.format(player)),
                  bbox_inches = 'tight')
    except:
        print('pass')
    plt.close('all')
print('done')
