# -*- coding: utf-8 -*-

"""
Created on Wed Dec 12 12:25:27 2018

@author: Mr.big

模块功能：主函数
"""
import pandas as pd
#from strategy import Strategy as st
from matplotlib import pyplot as plt
#from matplotlib.pylab import date2num

from datacenter import Data
from strategy import Strategy
from drawstockdata import DrawStockData
import strategy_doc

import sys
sys.path.append("..")
from conf import setting




class Stock(Data, Strategy, DrawStockData):
    pass
'''
class main():
    def __init__(self, codes, strategys):
        names = self.__dict__
        for k, v in codes.items():
            names['stock' + v] = Stock(name=k,code=v,start='2018-01-05')
            names['stock_df_' + v] = names['stock' + v].df
        
'''
#股票代码
codes = {
        '中兴通讯':'000063',
        '乐视网':'300104',
        '东方通信':'600776',
        '万科':'000002',
        '平安银行':'000001'
        }
codes2 = {
        '中兴通讯':'000063',
        }

final_data = pd.DataFrame({"名称": [],
                           "资金": [],
                           "收益": [],
                           "易数": []
                          })
#遍历股票
for k,v in codes.items():
    exec('stock{1} = Stock(name="{0}",code="{1}",start="2018-01-05")'.format(k,v))
    exec('stock_df_{0} = stock{0}.df'.format(v))
    exec('loock_bakc_{0} = stock{0}.loocback(strategy_doc.strategy)'.format(v))
    exec("pd_sell = loock_bakc_{0}['资产'][loock_bakc_{0}['操作']=='sell'].copy()".format(v))
    #print(pd_sell)
    if len(pd_sell)>0:
        final_data = final_data.append(pd.DataFrame({"名称": k,
                                                     "资金": pd_sell.iloc[-1],
                                                     "收益": (pd_sell.iloc[-1] - 10000) / 10000,
                                                     "易数": pd_sell.size
                                                    },index = [v]))
        #exec("loock{0}['资产'][loock{0}['操作']=='sell'].plot()".format(v))
        plt.plot(pd_sell.values,label=k+v)
print(final_data.sort_values(by='收益'))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.legend()
plt.show()

#stock000063.anal_rsi