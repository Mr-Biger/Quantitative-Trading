# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:25:27 2018
@author: Mr.big
模块功能：股票数据的采集和保存 提供正序时间数据
"""
import pandas as pd
import tushare as ts
import datetime,calendar
from matplotlib.pylab import date2num

class Data():
    def __init__(self,name= 'Mr.big', code= '600028', start= '2018-05-01',end= None, 
                 ktype= 'D', retry_count= 3, pause= 0.001, ma= [5,10,20],autype= 'qfq', index=False, locdata=True):
        """
        参数说明：
            name： 股票名字
            code：  股票代码，即6位数字代码，或者指数代码
                   （sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 
                   zxb=中小板 cyb=创业板）
                   
            start： 开始日期，格式YYYY-MM-DD 默认None
            end：   结束日期，格式YYYY-MM-DD 默认None
            ktype： 数据类型，D=日k线 W=周 M=月 5=5分钟 
                    15=15分钟 30=30分钟 60=60分钟，默认为D
                    
            retry_count： 当网络异常后重试次数，默认为3
            pause: 重试时停顿秒数，默认为0
            ma:    均线日期
            autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
            index:Boolean，是否是大盘指数，默认为False
            locdata:是否读取本地数据 默认True
        
        返回值说明：
            date：日期
            open：开盘价
            high：最高价
            close：收盘价
            low：最低价
            volume：成交量
            price_change：价格变动
            p_change：涨跌幅
            ma5：5日均价
            ma10：10日均价
            ma20:20日均价
            v_ma5:5日均量
            v_ma10:10日均量
            v_ma20:20日均量
            turnover:换手率[注：指数无此项]
        """
        self.name = name
        self.code = code
        self.start = start
        self.end = end
        self.ktype = ktype
        self.retry_count = retry_count
        self.pause = pause
        self.ma = ma
        self.autype = autype
        self.index = index
        self.locdata=locdata
        
        self.df = self.get_data()
        self.mat_data = self.pandas2mat(self.df)
    
    
    #获取数据
    def get_data(self):
        
        if self.locdata:
            
            try:
                print('正在读取[%s]本地数据。'%self.code)
                hist_data = pd.read_csv('../db/%s.csv'% self.code, sep=',', encoding='utf-8', index_col= 'date')
                print('正在校验日期')
                #校验日期
                start_date = self.start
                if self.end:
                    end_date = self.end
                else:
                    #end_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    #获取昨天日期
                    today = datetime.date.today()
                    yestday = today - datetime.timedelta(1) 
                    #判断是不是周末 如果是周末就继续向前取值
                    while yestday.weekday() in (calendar.SATURDAY, calendar.SUNDAY):
                        yestday -= datetime.timedelta(1)
                    end_date = yestday.strftime('%Y-%m-%d')
    
                if start_date not in hist_data.index or end_date not in hist_data.index:
                    print('正在更新本地数据……')
                    hist_data = self.get_hist_data(code= self.code, start= self.start, end= self.end, ktype= self.ktype, 
                                              retry_count= self.retry_count, pause= self.pause)
                    if len(hist_data)>0:
                        self.save_data(self.code, hist_data)
                else:
                    print('读取本地数据成功')
                    return hist_data[start_date:end_date]
                
            except Exception as e:
                print(e)
                print('读取本地数据失败！')
                print('正在获取网络数据……')
                hist_data = self.get_hist_data(code= self.code, start= self.start, end= self.end, ktype= self.ktype, 
                                          retry_count= self.retry_count, pause= self.pause)
                if len(hist_data)>0:
                        self.save_data(self.code, hist_data)
        else:
            hist_data = self.get_hist_data(code= self.code, start= self.start, end= self.end, ktype= self.ktype, 
                                      retry_count= self.retry_count, pause= self.pause)
            
        return hist_data
    #保存数据   
    def save_data(self, code, data):
        """
        参数说明：
            code: 股票代码
            data: datafram格式数据
        返回值说明：
            None
        """
        try:
            data.to_csv('../db/%s.csv'% code, sep=',', encoding= 'utf-8')
            print('保存[%s] 数据成功！'%code)
        except Exception as e:
            print(e)
    #获取历史数据
    def get_hist_data(self, code, start, end, ktype, retry_count, pause):
        try:
            hist_data = ts.get_hist_data(code=code, start=start, end=end, ktype=ktype, retry_count=retry_count, pause=pause)
            print('获取网络数据成功！')
        except Exception as e:
            print(e)
            print('获取网络数据失败')
            hist_data = []
        return hist_data[::-1] #反转时间序列
    #获取？？
    def get_basics_data(self):
        
        basics_data = ts.get_stock_basics()
        print (basics_data)
        return basics_data
    #获取复权数据
    def get_fuquan_data(self):
        
        '''
        参数说明：
            code:    string,股票代码 e.g. 600848
            start:   string,开始日期 format：YYYY-MM-DD 为空时取当前日期
            end:     string,结束日期 format：YYYY-MM-DD 为空时取去年今日
            autype:  string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
            index:   Boolean，是否是大盘指数，默认为False
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause :  int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
        
        返回值说明：
            date :   交易日期 (index)
            open :   开盘价
            high :   最高价
            close :  收盘价
            low :    最低价
            volume : 成交量
            amount : 成交金额
        '''
        fuquan_data = ts.get_h_data(code= self.code, start= self.start,end= self.end,
                                    retry_count= self.retry_count, pause= self.pause,
                                    autype= self.autype, index= self.index)
        print (fuquan_data)
        return fuquan_data
    #获取时时行情
    def get_shishi_data(self):
        '''
        返回值说明：
            code：代码
            name:名称
            changepercent:涨跌幅
            trade:现价
            open:开盘价
            high:最高价
            low:最低价
            settlement:昨日收盘价
            volume:成交量
            turnoverratio:换手率
            amount:成交量
            per:市盈率
            pb:市净率
            mktcap:总市值
            nmc:流通市值
        '''
        
        shsihi_data = ts.get_today_all()
        print (shsihi_data)
        return shsihi_data
    #获取历史分笔
    def get_lishifenbi_data(self):
        '''
        参数说明：
            code：股票代码，即6位数字代码
            date：日期，格式YYYY-MM-DD
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
        
        返回值说明：
            time：时间
            price：成交价格
            change：价格变动
            volume：成交手
            amount：成交金额(元)
            type：买卖类型【买盘、卖盘、中性盘】
        '''
        fenbi_data = ts.get_tick_data(code= self.code, date= '2018-08-08',
                                      retry_count= self.retry_count, pause= self.pause)
        print (fenbi_data)
        return fenbi_data
    #获取实时分笔
    def get_shishifenbi_data(self):
        '''
        参数说明：
            symbols：6位数字股票代码，或者指数代码（sh=上证指数 sz=深圳成指 
            hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板） 
            可输入的类型：str、list、set或者pandas的Series对象 
            可以是列表
        
        返回值说明:
            0：name，股票名字
            1：open，今日开盘价
            2：pre_close，昨日收盘价
            3：price，当前价格
            4：high，今日最高价
            5：low，今日最低价
            6：bid，竞买价，即“买一”报价
            7：ask，竞卖价，即“卖一”报价
            8：volume，成交量 maybe you need do volume/100
            9：amount，成交金额（元 CNY）
            10：b1_v，委买一（笔数 bid volume）
            11：b1_p，委买一（价格 bid price）
            12：b2_v，“买二”
            13：b2_p，“买二”
            14：b3_v，“买三”
            15：b3_p，“买三”
            16：b4_v，“买四”
            17：b4_p，“买四”
            18：b5_v，“买五”
            19：b5_p，“买五”
            20：a1_v，委卖一（笔数 ask volume）
            21：a1_p，委卖一（价格 ask price）
            ...
            30：date，日期；
            31：time，时间；
        '''
        sshifenbi_data = ts.get_realtime_quotes(symbols= self.code)
        
        print (sshifenbi_data)
        return sshifenbi_data
    #获取当日历史分笔
    def get_dangrifenbi_data(self):
        '''
        参数说明：
            code：股票代码，即6位数字代码
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
            
        返回值说明:
            time：时间
            price：当前价格
            pchange:涨跌幅
            change：价格变动
            volume：成交手
            amount：成交金额(元)
            type：买卖类型【买盘、卖盘、中性盘】
        '''
        drifenbi_data = ts.get_today_ticks(code= self.code,
                                           retry_count= self.retry_count, pause= self.pause)
        
        print (drifenbi_data)
        return drifenbi_data
    #获取大盘指数行情
    def get_dapan_data(self):
        '''
        返回值说明：
            code:指数代码
            name:指数名称
            change:涨跌幅
            open:开盘点位
            preclose:昨日收盘点位
            close:收盘点位
            high:最高点位
            low:最低点位
            volume:成交量(手)
            amount:成交金额（亿元）
        '''
        dapan_data = ts.get_index()
        
        print(dapan_data)
        return dapan_data
    #获取大单数据
    def get_dadan_data(self):
        '''
        参数说明：
            code：股票代码，即6位数字代码
            date:日期，格式YYYY-MM-DD
            vol:手数，默认为400手，输入数值型参数
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
        
        返回值说明：    
            code：代码
            name：名称
            time：时间
            price：当前价格
            volume：成交手
            preprice ：上一笔价格
            type：买卖类型【买盘、卖盘、中性盘】
        '''
        dadan_data = ts.get_sina_dd(code= self.code, date= '2018-08-08', vol= 400,
                                    retry_count= self.retry_count, pause= self.pause)
        print(dadan_data)
        return dadan_data
    #Pandas 转换为 mat
    def pandas2mat(self,pd_data):
        datafram = pd_data[['open','close','high','low','volume','v_ma10']]
        index = datafram.index.astype('datetime64[ns]')#将str转换为datetime
        datafram.insert(loc=0,column='date',value=index)
        
        #datafram.index = datafram['date']

        mat_data = datafram.as_matrix()#DataFram to matrix
        mat_data[:,0] = list(map(lambda x: date2num(x),mat_data[:,0]))
        return mat_data #矩阵数据