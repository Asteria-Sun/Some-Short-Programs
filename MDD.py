'''最大回撤计算'''
import numpy as np
import pandas as pd
import datetime

#随机趋势+持续上涨的趋势
price = 2 + np.random.randn(21) + np.linspace(0,2,21)
#设置日期
date = [datetime.date(2020,12,x) for x in range(2,23)]
MDD_df = pd.DataFrame({'date':date,'price':price})
#简单收益率没减1是为了方便连乘
MDD_df['return+1'] = MDD_df['price']/MDD_df['price'].shift(1)
MDD_df['cum_return'] = MDD_df['return+1'].cumprod()
MDD_df = MDD_df.dropna(axis=0, how='any')
MDD_df = MDD_df.reset_index(drop = True)
MDD_df['return_max'],MDD_df['return_min'] = MDD_df['cum_return'],MDD_df['cum_return']

l=len(MDD_df)
#求当前最大/最小累积收益率
for i in range(1,l):
    if MDD_df['return_max'][i] < MDD_df['return_max'][i-1]:
        MDD_df['return_max'][i] = MDD_df['return_max'][i-1]
    if MDD_df['return_min'][i] > MDD_df['return_min'][i-1]:
        MDD_df['return_min'][i] = MDD_df['return_min'][i-1]
#求最大差值（必然出现在当前最大累积收益和最小累积收益之间）
MDD_df['spread_max'] = MDD_df['return_max'] - MDD_df['return_min']
#根据定义求回撤率
MDD_df['d_rate'] = MDD_df['spread_max']/MDD_df['return_max']
#最大回撤率
mdd = MDD_df['d_rate'].max()
