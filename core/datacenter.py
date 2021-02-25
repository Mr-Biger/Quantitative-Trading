# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:25:27 2018

@author: Mr.big

模块功能：股票数据的采集和保存 提供正序时间数据
"""
import pandas as pd
#import tushare as ts #shixiao
import baostock as bs

import datetime,calendar
from matplotlib.pylab import date2num

class DataCenter():
    
#    def __init__(self,name='',code = "sh.600000",fields="date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",start_date='2020-01-02',end_date='2021-02-20',frequency="d",adjustflag="3",locdata=True):
#        
#        self.name = name
#        self.code = code
#        self.fields = fields
#        self.start_date = start_date
#        self.end_date = end_date
#        self.frequency = frequency
#        self.adjustflag = adjustflag
#        self.locdata = locdata
#        
#        self.df = self.get_data()
#        self.mat_data = self.pandas2mat()

    #获取数据
    def get_data(self):
        
        if self.locdata:
            
            try:
                print('正在读取[%s]本地数据。'%self.code)
                hist_data = pd.read_csv('../db/%s.csv'% self.code, sep=',', encoding='utf-8', index_col= 'date')
                print('正在校验日期')
                
                #校验日期
                
                start_date = self.start_date
                if self.end_date:
                    end_date = self.end_date
                else:
                    #end_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    #获取昨天日期
                    today = datetime.date.today()
                    yestday = today - datetime.timedelta(1) 
                    #判断是不是周末 如果是周末就继续向前取值
                    while yestday.weekday() in (calendar.SATURDAY, calendar.SUNDAY):
                        yestday -= datetime.timedelta(1)
                    end_date = yestday.strftime('%Y-%m-%d')
                
                start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d')
                while start_date.weekday() in (calendar.SATURDAY, calendar.SUNDAY):
                    start_date += datetime.timedelta(1)
                start_date=start_date.strftime('%Y-%m-%d')
                
                end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d')
                while end_date.weekday() in (calendar.SATURDAY, calendar.SUNDAY):
                    end_date -= datetime.timedelta(1)
                end_date = end_date.strftime('%Y-%m-%d')
                    
                print(start_date,end_date)
    
    
    
    
                if start_date not in hist_data.index or end_date not in hist_data.index:
                    print('正在更新本地数据……')
                    hist_data = self.get_hist_data()
                    if len(hist_data)>0:
                        self.save_data(hist_data)
                else:
                    print('读取本地数据成功')
                    return hist_data[start_date:end_date]
                
            except Exception as e:
                print(e)
                print('读取本地数据失败！')
                print('正在获取网络数据……')
                hist_data = self.get_hist_data()
                if len(hist_data)>0:
                        self.save_data(hist_data)
        else:
            hist_data = self.get_hist_data()
            
        return hist_data        
    #保存数据   
    def save_data(self,hist_data):
        """
        参数说明：
            code: 股票代码
            data: datafram格式数据
        返回值说明：
            None
        """
        try:
            hist_data.to_csv('../db/%s.csv'% self.code, sep=',', encoding= 'utf-8')
            print('保存[%s] 数据成功！'%self.code)
        except Exception as e:
            print(e)
    
    #获取历史数据
    def get_hist_data(self):
            
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg)
        
        try:        
            rs = bs.query_history_k_data_plus(
                        code = self.code,
                        fields = self.fields,
                        start_date = self.start_date,
                        end_date = self.end_date,
                        frequency = self.frequency,
                        adjustflag = self.adjustflag)
            
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            
            hist_data = pd.DataFrame(data_list, columns=rs.fields)
            hist_data=hist_data.set_index('date')
            hist_data[rs.fields[2:]] =  hist_data[rs.fields[2:]].apply(pd.to_numeric)
            print('获取网络数据成功！')
        except Exception as e:
            print(e)
            print('获取网络数据失败')
            hist_data = []
        
        finally:
            bs.logout()
            return hist_data#[::-1] #反转时间序列
    

    #Pandas 转换为 mat
    def pandas2mat(self):
        
        datafram = self.df.loc[:,['open','close','high','low','volume']]
        index = datafram.index.astype('datetime64[ns]')#将str转换为datetime
        datafram.insert(loc=0,column='date',value=index)
        
        #datafram.index = datafram['date']

        mat_data = datafram.values#as_matrix()#DataFram to matrix
        mat_data[:,0] = list(map(lambda x: date2num(x),mat_data[:,0]))
        return mat_data #矩阵数据
    
if __name__ == "__main__":
    data = DataCenter()
    hisdata = data.df
    matdata = data.mat_data
    
