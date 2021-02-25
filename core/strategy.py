# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:25:27 2018

@author: Mr.big

模块功能：股票数据的分析
"""
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import numpy as np

#股票指标计算类
class Calculate():
    #统计分析
    #计算收益率
    @property
    def calc_yield_rate(self, returns_num=1):
        """
        参数说明：
            df: 股票历史行情（时间正序）
            returns_num: 股票名字
        返回值说明：
            yield_rate:收益率
        """
        #收盘价格
        close = self.df['close']
        #收益率
        yield_rate = (close - close.shift(returns_num)) / close.shift(returns_num)
        yield_rate.fillna(0,inplace=True)
        #print (returns)
        return yield_rate
    
    #计算未来10天中6天上涨概率
    @property
    def calc_rise_prob(self):
        returns = self.calc_yield_rate
        p = len(returns[returns>0]) / len(returns)
        prob = stats.binom.pmf(6, 10, p)
        return prob
        
    #计算收益率均值的参数估计
    @property
    def calc_yield_rate_range(self):
        yield_rate = self.calc_yield_rate
        yield_rate.hist()
        mu = yield_rate.mean()
        sigma = yield_rate.std()
        plt.plot()
        pass
        
    #############股票指标计算############
    #计算macd
    #EMA计算方法请参考指数平滑均线文档，这里的平滑系数参数以12日，26日，9日参数为例。参数大家可以进行修改。
    #12日EMA的计算：EMA12 = 前一日EMA12 X 11/13 + 今日收盘 X 2/13
    #26日EMA的计算：EMA26 = 前一日EMA26 X 25/27 + 今日收盘 X 2/27
    #差离值（DIF）的计算： DIF = EMA12 - EMA26 。
    #根据差离值计算其9日的EMA，即离差平均值，是所求的DEA值。今日DEA = （前一日DEA X 8/10 + 今日DIF X 2/10）
    #DIF与它自己的移动平均之间差距的大小BAR=（DIF-DEA）*2，即为MACD柱状图。
    #买卖原则为：
    #DIF、DEA均为正，DIF向上突破DEA，买入信号参考。
    #DIF、DEA均为负，DIF向下突破DEA，卖出信号参考。
    
    def calc_macd(self,short=12,long=26,M=9):  
        """
        参数说明：
            short:快速移动平均线日期 默认 12
            long: 慢速移动平均线日期 默认 26
            M: 离差值日期 默认 9
        返回值说明：
            sema:快速移动平均线（值）
            lema：慢速移动平均线（值）
            diff：离差值
            dea：离差平均值
            macd：指数平滑异同移动平均线（值）
        """
        #创建临时表格
        temp_df = pd.DataFrame()
        temp_df['sema'] = self.df['close'].ewm(span=short).mean()
        temp_df['lema'] = self.df['close'].ewm(span=long).mean()
        temp_df.fillna(0,inplace = True)
        
        self.df['diff'] = temp_df['sema'] - temp_df['lema']
        self.df['dea'] = self.df['diff'].ewm(span=M).mean()
        self.df['macd'] = 2*(self.df['diff'] - self.df['dea'])
        self.df.fillna(0,inplace = True)
    
    #计算kdj
    #KDJ指标的计算方法
    #指标KDJ的计算比较复杂，首先要计算周期（n日、n周等）的RSV值，即未成熟随机指标值，
    #然后再计算K值、D值、J值等。以日KDJ数值的计算为例，其计算公式为
    #n日RSV=（Cn－Ln）÷（Hn－Ln）×100
    #式中，Cn为第n日收盘价；Ln为n日内的最低价；Hn为n日内的最高价。RSV值始终在1—100间波动。
    #其次，计算K值与D值：
    #当日K值=2/3×前一日K值＋1/3×当日RSV
    #当日D值=2/3×前一日D值＋1/3×当日K值
    #若无前一日K 值与D值，则可分别用50来代替。
    #以9日为周期的KD线为例。首先须计算出最近9日的RSV值，即未成熟随机值，计算公式为
    #9日RSV=（C－L9）÷（H9－L9）×100<
    #式中，C为第9日的收盘价；L9为9日内的最低价；H9为9日内的最高价。
    #K值=2/3×前一日 K值＋1/3×当日RSV
    #D值=2/3×前一日K值＋1/3×当日RSV
    #若无前一日K值与D值，则可以分别用50代替。
    #<需要说明的是，式中的平滑因子1/3和2/3是可以人为选定的,不过目前已经约定俗成，固定为1/3和2/3。
    #在大多数股市分析软件中，平滑因子已经被设定为1/3和2/3，不需要作改动。另外，一般在介绍KD时，往往还附带一个J指标。
    #J指标的计算公式为：
    #J=3D—2K
    #实际上，J的实质是反映K值和D值的乖离程度，从而领先KD值找出头部或底部。J值范围可超过100。
    def calc_kdj(self,N=9,M=2):
        """
        参数说明：
            N:
            M: 
        返回值说明：
            KDJ_K:
            KDJ_D:
            KDJ_J:
        """
        low_list = self.df['low'].rolling(window=N).min()
        low_list.fillna(value=self.df['low'].expanding(min_periods=1).min(),inplace=True)
        high_list = self.df['high'].rolling(window=N).max()
        high_list.fillna(value=self.df['high'].expanding(min_periods=1).max(),inplace=True)
        rvs = (self.df['close'] - low_list) / (high_list - low_list) * 100
        self.df['KDJ_K'] = rvs.ewm(com=M,min_periods=0,adjust=True,ignore_na=False).mean()
        self.df['KDJ_D'] = self.df['KDJ_K'].ewm(com=2,min_periods=0,adjust=True,ignore_na=False).mean()
        self.df['KDJ_J'] = 3 * self.df['KDJ_K'] - 2 * self.df['KDJ_D']
        self.df.fillna(0,inplace=True)
    #计算rsi
    def calc_rsi(self,N=24, N1=6):        
        self.df['value'] = self.df['close'] - self.df['close'].shift(1)
        self.df.fillna(0,inplace=True)
        
        value1=self.df['value'].copy()
        value1[value1<0]=0
        self.df['value1']=value1
        #self.df['value1'] = self.df['value']
        #self.df['value1'][self.df['value1']<0]=0
        value2=self.df['value'].copy()
        value2[value2>0]=0
        self.df['value2']=value2        
        
        #self.df['value2']= self.df['value']
        #self.df['value2'][self.df['value2']>0]=0
        
        self.df['plus'+str(N)] = self.df['value1'].rolling(window=N,center=False).sum()
        self.df['plus'+str(N1)] = self.df['value1'].rolling(window=N1,center=False).sum()
        
        self.df['minus'+str(N)] = self.df['value2'].rolling(window=N,center=False).sum()
        self.df['minus'+str(N1)] = self.df['value2'].rolling(window=N1,center=False).sum()
        
        self.df.fillna(0,inplace=True)
        
        self.df['rsi'+ str(N)] = self.df['plus'+str(N)] / (self.df['plus'+str(N)] - self.df['minus'+str(N)]) * 100
        self.df['rsi'+ str(N1)] = self.df['plus'+str(N1)] / (self.df['plus'+str(N1)] - self.df['minus'+str(N1)]) * 100
        
        self.df.fillna(0,inplace=True)
    #计算cci
    def calc_cci(self,N=14):
        self.df['tp'] = (self.df['high'] + self.df['low'] + self.df['close']) / 3
        self.df['mac'] = self.df['tp'].rolling(window=N,center=False).mean()
        self.df.fillna(0,inplace=True)
        self.df['md'] = 0.0
        for i in range(len(self.df) - N):
            self.df['md'][i+N-1] = self.df['close'][i:i+N-1].mad()
        self.df['cci'] = (self.df['tp'] - self.df['mac']) / (self.df['md'] * 0.015)
    #计算wr
    def calc_wr(self,N=4):
        low_list = self.df['low'].rolling(window=N).min()
        low_list.fillna(value=self.df['low'].expanding(min_periods=1).min(),inplace=True)
        high_list = self.df['high'].rolling(window=N).max()
        high_list.fillna(value=self.df['high'].expanding(min_periods=1).max(),inplace=True)
        self.df['w%r'] = (high_list - self.df['close']) / (high_list - low_list) * 100
    #计算cr
    def calc_cr(self,N=7):
        self.df['ym'] = 0.0
        for i in range(len(self.df)):
            if i > 0:
                self.df['ym'][i] = (self.df['close'][i-1] * 2 + self.df['high'][i-1] + self.df['low'][i-1]) / 4
        self.df['p1'] = (self.df['high'] - self.df['ym']).rolling(window=N).sum()
        self.df['p2'] = (self.df['ym'] - self.df['low']).rolling(window=N).sum()
        self.df['cr'] = self.df['p1'] / self.df['p2'] * 100
        self.df.fillna(0,inplace=True)
    #计算价格动量
    @property
    def calc_momentum(self):
        self.df['lag5_close'] = self.df['close'].shift(35)
        self.df['momentum'] = self.df['close'] - self.df['lag5_close']
        self.df.fillna(0,inplace=True)

#数据分析类    
class Analysis(Calculate):
    @property
    def anal_macd(self):
        
        self.calc_macd()
        #macd = self.sd.df[['diff','dea']].copy()
        #macd = self.df.copy()
        #bar = self.df[['macd']].copy()
        
        #计算曲线距离扩张收缩趋势
        self.df['distance_macd'] = self.df['diff'] - self.df['dea']
        #macd['trend'] = macd['distance'].rolling(window=5).sum() #5日平均距离会影响判断及时性
        #macd.fillna(0,inplace=True)
        #macd['trend_sign'] = np.abs(macd['trend']) - np.abs(macd['trend'].shift(1))
        #曲线的远近趋势 1：变远 -1：变近
        self.df['trend_sign_macd'] = np.abs(self.df['distance_macd']) - np.abs(self.df['distance_macd'].shift(1))
        self.df.fillna(0,inplace=True)
        self.df['trend_sign_macd'] = np.sign(self.df['trend_sign_macd'])
        
        #计算金叉死叉
        #判断diff dea 高度 1：diff在dea上方 -1 diff在dea下方
        self.df['distance_sign_macd'] = np.sign(self.df['distance_macd'])
        #diff dea 上下交叉变换点 2：diff上穿dea -2：diff下穿dea
        self.df['cross_macd'] = self.df['distance_sign_macd'] - self.df['distance_sign_macd'].shift(1)
        #print(macd.where(macd['cross'] != 0).dropna())
        #print(bar)
        self.df.fillna(0,inplace=True)
        #macd['bs'] = macd['trend_sign'] + macd['distance_sign'] + macd['cross']
        #return macd
    
    @property
    def anal_rsi(self):
        self.calc_rsi()
        self.df['distance_rsi'] = self.df['rsi6'] - self.df['rsi24']
        self.df['trend_sign_rsi'] = np.abs(self.df['distance_rsi']) - np.abs(self.df['distance_rsi'].shift(1))
        self.df.fillna(0,inplace=True)
        self.df['trend_sign_rsi'] = np.sign(self.df['trend_sign_rsi'])
        self.df['distance_sign_rsi'] = np.sign(self.df['distance_rsi'])
        self.df['cross_rsi'] = self.df['distance_sign_rsi'] - self.df['distance_sign_rsi'].shift(1)
        self.df.fillna(0,inplace=True)
        
    @property
    def anal_kdj(self):
        self.calc_kdj()
    
    
    @property
    def anal_momentum(self):
        self.calc_momentum
        
        

class Strategy(Analysis):
    #回测函数
    def loocback(self,strategy,cash=10000, port_value=1.0 ,batch=100 ,stoploss=.2 ,stop_switch =False):
        """
        参数说明：
            strategy:字典结构｛funcname:{ #函数名字
                                        buy:[],#对应的买入策略
                                        sell:[]#对应的卖出策略
                            }｝
            
            ##data: 带有bsp(买卖点)的datafram数据表 1：buy -1：shell 0：None
            cash：资金
            port_value：仓位
            batch：一手股票数量
            stoploss：止损点
            stop_switch：止损开关
        返回值说明：
            loopback_data：回测数据表
        """
        #根据输入参数strategy中funcname 调用相应函数
        buy = ''
        sell = ''
        for k,v in strategy.items():
            print('调用'+ k)
            exec("self.{}".format(k))
            buy += v.get('buy', '')
            sell += v.get('sell', '')
            print('买入决策：' + buy)
            print('卖出决策：' + sell)
            
        #设计策略买卖点 bsp
        l = len(self.df)
        bsp = np.zeros(l)
        for i in range(l-1):      
            #if macd['trend_sign'][i]==-1 and macd['distance_sign'][i]==-1 and macd['cross'][i]==0:
            exec("if all([{}]):\n    bsp[i+1] = 1".format(buy))
                #bsp[i+1] = 1 #头一天的信号 第二天才能参考操作
            #elif macd['trend_sign'][i]==1 and macd['distance_sign'][i]==1 and macd['cross'][i]==0:
            exec("if all([{}]):\n    bsp[i+1] = -1".format(sell))
                #bsp[i+1] = -1 #头一天的信号 第二天才能参考操作
            #else:
                #pass
        
        self.df.insert(0,'bsp', bsp)
        
        loopback_data = pd.DataFrame({"资产": [],
                                      "操作": [],
                                      "手数": [],
                                      "股数": [],
                                      "价格": [],
                                      "利点": [],
                                      "利润": [],
                                      "止损": []
                                      })
    
        
        
        
        batches = 0  #初始仓位
        price = None #初始化价格参数
        #share_profit = 0 #初始利点
        #profit =0 #初始化利润
        handle = None #初始操作
        
        data = self.df
        
        for index, row in data.iterrows():
            stop_trig ='False' #初始化止损信息
            if row['bsp'] == 1:
                shoushu = np.floor(cash *port_value) //np.ceil(batch *row["open"])
                #以开盘价格作为买入价格计算买入手数
                if shoushu:
                    handle = 'buy'
                    profit = 0
                    share_profit=0
                    buy_value = row['open']
                    price = buy_value
                    batches += shoushu #股数
                    ##################
                    cash = cash - price*shoushu*batch
                    #trade_val = batches * batch * buy_value #买股票花掉的钱
                else:
                    continue
            elif row['bsp'] ==-1:
                if batches :
                    handle = 'sell'
                    sell_value = row['open']
                    price = sell_value
                    share_profit = sell_value - buy_value
                    profit =share_profit *batches *batch #利润
                    shoushu = batches
                    batches = 0
                    ##################
                    cash = cash + price*shoushu*batch
                else:
                    continue
            elif row['bsp'] == 0 and stop_switch:
                if batches :
                    if row['low'] < (1 - stoploss) * buy_value:
                        handle = 'st_sell'
                        share_profit = -np.round((stoploss) *buy_value, 2)
                        price = (1- stoploss) * price
                        stop_trig ='True'
                        profit =share_profit *batches *batch #利润
                        shoushu = batches
                        batches = 0
                        
                        ##################
                        cash = cash + price*shoushu*batch
                    else:
                        continue
                else:
                    continue
            else:
                continue
            
            #profit =share_profit *batches *batch #利润
            loopback_data = loopback_data.append(pd.DataFrame({
                                                "资产": cash,
                                                "操作": handle,
                                                "手数": shoushu,
                                                "股数": batches,
                                                "价格": price,
                                                "利点": share_profit,
                                                "利润": profit,
                                                "止损": stop_trig
                                                }, index =[index]))
            #cash =max(0, cash +profit)
        #loopback_data["资产"].plot()
        columns = ["资产","操作","手数","股数","价格","利点","利润","止损"]
        loopback_data = loopback_data.loc[:,columns]#安照指定顺序输出
        self.loopback_data = loopback_data
        return loopback_data
            
        
    
