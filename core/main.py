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

from datacenter import DataCenter
from strategy import Strategy
from drawstockdata import DrawStockData
import strategy_doc

import sys
sys.path.append("..")
from conf import setting


class Stock(DataCenter, Strategy, DrawStockData):

    def __init__(self,name='',code = "sh.600000",fields="date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",start_date='2020-01-02',end_date='2021-02-21',frequency="d",adjustflag="3",locdata=True):
        
        self.name = name
        self.code = code
        self.fields = fields
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.adjustflag = adjustflag
        self.locdata = locdata
        
        self.df = self.get_data()
        self.mat_data = self.pandas2mat()
        

def run():
    #股票池
    stockpool={}
    
    #回测结果
    final_data = pd.DataFrame({"名称": [],
                               "资金": [],
                               "收益率": [],
                               "易手数": [],
                               "均收益率":[]
                              })
    
    #遍历股票 回测
    for k,v in setting.codes.items():
        
        stock = stockpool.setdefault(k,{})
        
        stock['instance'] = Stock(name=k,code=v)
        stock['df'] = stock['instance'].df
        stock['loopback_data'] = stock['instance'].loocback(strategy_doc.strategies[setting.strategy],setting.cash,setting.port_value,setting.batch,setting.stoploss,setting.stop_switch)
        #pd_sell = stock['loopback_data']['资产'][stock['loopback_data']['操作']=='sell'].copy()
        #pd_sell = stock['loopback_data']['资产'][stock['loopback_data']['操作'].str.contains('sell')].copy()
        
        pd_sell = stock['loopback_data']['资产'][(stock['loopback_data']['操作']=='sell') | (stock['loopback_data']['操作']=='st_sell')].copy()
        
        #exec('stock{0} = Stock(name="{0}",code="{1}")'.format(k,v))
        ##exec('stock_df_{0} = stock{0}.df'.format(k,v)) 
        #exec('loock_bakc_{0} = stock{0}.loocback(strategy_doc.{1},{2},{3},{4},{5})'.format(k,setting.strategy,setting.cash,setting.port_value,setting.batch,setting.stoploss))
        #exec("pd_sell = loock_bakc_{0}['资产'][loock_bakc_{0}['操作']=='sell'].copy()".format(k))
        #print(pd_sell)
        if len(pd_sell)>0:

            if len(pd_sell)>3:
                l = len(pd_sell)
                buchang = l//3
                v1 = pd_sell.iloc[buchang]
                v2 = pd_sell.iloc[2*buchang]
                v3 = pd_sell.iloc[-1]
                
                res = (((v3-v2)/v2) - ((v2-v1)/v1))**2/2
            else:
                res = 1
                
            final_data = final_data.append(pd.DataFrame({"名称": k,
                                                         "资金": pd_sell.iloc[-1],
                                                         "收益率": (pd_sell.iloc[-1] - setting.cash) / setting.cash,
                                                         "易手数": pd_sell.size,
                                                         "均收益率":res
                                                        },index = [v]))                
                
            #绘制结果
            if setting.drawres:
                plt.plot(pd_sell.values,label=k+v)
    #绘制结果
    if setting.drawres:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.legend()
        plt.show()
    
    #打印结果
    print(final_data.sort_values(by='收益率'))
    
    return stockpool

if __name__ == "__main__":
    stockpool=run()
