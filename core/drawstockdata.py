# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import pandas as pd
import numpy as np
from matplotlib.pylab import date2num
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY

class Shape():
    @property
    def morinig_star(self):
        self.df['cl-op'] = self.df['close'] - self.df['open']
        self.df['lag1clop'] = self.df['cl-op'].shift(1)
        self.df['lag2clop'] = self.df['cl-op'].shift(2)
        
        de = self.df['cl-op'].describe()
        morning_star_shape = [0,0,0]
        
        for i in range(3, len(self.df['cl-op'])):
            if all ([
                     self.df['lag2clop'][i]<de['25%'],
                     #self.df['lag2clop'][i]<0,
                     abs(self.df['lag1clop'][i]<de['50%']),
                     self.df['cl-op'][i]>0,
                     abs(self.df['cl-op'][i])>abs(self.df['lag2clop'][i]*0.5)]):
                morning_star_shape.append(1)
            else:
                morning_star_shape.append(0)
                
        self.df.insert(0,'morning_star_shape', morning_star_shape)
        
        self.df['lag1open'] = self.df['open'].shift(1)
        self.df['lag1close'] = self.df['close'].shift(1)
        self.df['lag2close'] = self.df['close'].shift(2)
        
        doji = [0,0,0]
        
        for i in range(3,len(self.df['open']),1):
            if all([self.df['lag1open'][i]<self.df['open'][i],
                    self.df['lag1open'][i]<self.df['lag2close'][i],
                    self.df['lag1close'][i]<self.df['open'][i],
                    self.df['lag1close'][i]<self.df['lag2close'][i]
            ]):
                doji.append(1)
            else:
                doji.append(0)
            
        self.df.insert(0,'doji', doji)
        
        self.df['ret'] = (self.df['close'] / self.df['close'].shift(1)) -1
        self.df['lag1ret'] = self.df['ret'].shift(1)
        self.df['lag2ret'] = self.df['ret'].shift(2)
        
        trend = [0,0,0]
        for i in range(3,len(self.df['ret'])):
            if all([self.df['lag1ret'][i]<0,self.df['lag2ret'][i]<0]):
                trend.append(1)
            else:
                trend.append(0)
        self.df.insert(0,'trend', trend)
        
        starsig = []
        for i in range(len(self.df['ret'])):
            if all([ self.df['shape'][i]==1,self.df['doji'][i]==1,self.df['trend'][i]==1]):
                starsig.append(1)
            else:
                starsig.append(0)
        
        self.df.insert(0,'starsig', starsig)
    def evening_star(self):
        pass
        

class DrawStockData(Shape):
    @property   
    def draw_k(self):
        fig, ax = plt.subplots(figsize=(15,5))
        fig.subplots_adjust(bottom=0.5)
        mpf.candlestick_ochl(ax, self.mat_data, width=0.6, colorup='r', colordown='k', alpha=1.0)
        #candlestick_ochl : time must be in float days format - see date2num
        plt.grid(True) 
        plt.xticks(rotation=30)# 设置日期刻度旋转的角度
        plt.title(self.name + ':' + self.code)
        plt.xlabel('Date')
        plt.ylabel('Price')
        # x轴的刻度为日期
        ax.xaxis_date ()
        plt.show()
        ###candlestick_ochl()函数的参数
        # ax 绘图Axes的实例
        # mat_wdyx 价格历史数据
        # width    图像中红绿矩形的宽度,代表天数
        # colorup  收盘价格大于开盘价格时的颜色
        # colordown   低于开盘价格时矩形的颜色
        # alpha      矩形的颜色的透明度
    @property
    def draw_k_easy(self):
        fig, ax = plt.subplots(figsize=(15,5))
        mpf.plot_day_summary_oclh(ax, self.mat_data,colorup='r', colordown='k')
        plt.grid(True)
        ax.xaxis_date()
        plt.title(self.name + ':' + self.code)
        plt.ylabel('Price')
        plt.show()
    @property
    def draw_k_v(self):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(15,8))
        mpf.candlestick_ochl(ax1, self.mat_data, width=0.5, colorup = 'r', colordown = 'k')
        ax1.set_title(self.name + ':' + self.code)
        ax1.set_ylabel('Price')
        ax1.grid(True)
        ax1.xaxis_date()
        plt.bar(self.mat_data[:,0], self.mat_data[:,5], width= 0.5)# ? mat_data[:,0] - 0.25
        ax2.set_ylabel('Volume')
        ax2.grid(True)
        plt.show()
    @property    
    def stock_return(self):#相对于第一天的股价波动
#        data_info_pd = self.df.set_index(['date'])#index 由project更改为时间
        stocks = pd.DataFrame({self.name:self.df['close'][::-1]})#时间由远及近
        stocks_return = stocks.apply(lambda x: x / x[0])
        stocks_return.plot(grid = True).axhline(y = 1, color = "black", lw = 2)
        plt.show()
    @property
    def change(self):#######################
#        data_info_pd = self.df.set_index(['date'])#index 由project更改为时间
        stocks = pd.DataFrame({self.name:self.df['close'][::-1]})#时间由远及近
        stocks_change = stocks.apply(lambda x: np.log(x) - np.log(x.shift(1)))#shift（1） 后退一天
        stocks_change.head()
        stocks_change.plot(grid = True).axhline(y = 0, color = "black", lw = 2)
        plt.show()
    @property
    def pandas_candlestick_ohlc(self):
        self.morinig_star
        stock_data = self.df
        #print(stock_data.columns)
        stock_data.index = stock_data.index.astype('datetime64[ns]')#index转为timedata
        #backtest = self.huice_shouyi()
        backtest = self.loopback_data.copy()
        backtest.index = backtest.index.astype('datetime64[ns]')#index转为timedata
     
        # 设置绘图参数，主要是坐标轴 
        mondays = WeekdayLocator(MONDAY) 
        alldays = DayLocator()   
        dayFormatter = DateFormatter('%d')
        
        #创建图纸
        fig = plt.figure(figsize=(15,8))
        
        def call_back(event):
            axtemp=event.inaxes
            x_min, x_max = axtemp.get_xlim()
            fanwei = (x_max - x_min) / 10
            if event.button == 'up':
                axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
                print('up')
            elif event.button == 'down':
                axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
                print('down')
            fig.canvas.draw_idle()  # 绘图动作实时反映在图像上
        fig.canvas.mpl_connect('scroll_event', call_back)
        fig.canvas.mpl_connect('button_press_event', call_back)
        
        
        ax1 = plt.subplot2grid((7,1), (0,0), rowspan=1, colspan=1)
        plt.ylabel('Capital')
        ax2 = plt.subplot2grid((7,1), (1,0), rowspan=3, colspan=1,sharex = ax1)
        #plt.xlabel('Date')
        plt.ylabel('Price')
        
        ax4 = plt.subplot2grid((7,1), (4,0), rowspan=1, colspan=1,sharex = ax1)
        
        ax3 = plt.subplot2grid((7,1), (5,0), rowspan=2, colspan=1,sharex = ax1)
        ax3.set_ylabel('Volume')
        
        #fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(15,8))
        #fig, ax = plt.subplots()
        #fig.subplots_adjust(bottom=0.2)

        #ax1.plot(backtest["End Port. Value"])  #zheli yao genggai !!!!~~~~~~~~  
        #绘制总资产
        ax1.plot(backtest["资产"][backtest['操作']=='sell'])
        ax1.grid(True)
        plt.setp(ax1.get_xticklabels(), visible=False)# 隐藏x轴标签
                
        if stock_data.index[-1] - stock_data.index[0] < pd.Timedelta('730 days'):
            weekFormatter = DateFormatter('%b %d')  
            ax2.xaxis.set_major_locator(mondays)
            ax2.xaxis.set_minor_locator(alldays)
        else:
            weekFormatter = DateFormatter('%b %d, %Y')
        ax2.xaxis.set_major_formatter(weekFormatter)
        ax2.grid(True)
     
        # 创建K线图   
        stock_array = np.array(stock_data.reset_index()[['date','open','high','low','close']])
        stock_array[:,0] = date2num(stock_array[:,0])
        candlestick_ohlc(ax2, stock_array, colorup = "red", colordown="green", width=0.4)
        plt.setp(ax2.get_xticklabels(), visible=False)# 隐藏x轴标签
        
        #买卖点绘制
        #ax2.plot(backtest['价格'],marker='o',color= ['r' if x=='sell' else 'b' for x in backtest['操作'] ] )
        for index, row in backtest.iterrows():
            col = 'c'
            sty = 'o'
            if row['操作']=='sell':
                col='m'
                sty='o'
            ax2.plot(index,row['价格'],sty,color=col )
        #绘制早晨之星
        if 'starsig' in stock_data:
            for index, row in stock_data.iterrows():
                if row['starsig'] == 1:
                    ax2.plot(index,row['open'],'*',color='y' )
                    
            
        # 可同时绘制其他折线图
        #绘制均线
        if self.ma is not None:
            for each in self.ma:
                ax2.plot(stock_data['ma' + str(each)], label=['ma' + str(each)],LineWidth=0.5)            
            ax2.legend()  #这里会报错
        #You must have plot the candle plots and the volume
        #before plotting the SMA. The candle plot doesn't have
        #any labeled object, when you call the plt.legend(),
        #it tries to plot a label for every plot on the current axes.
        #Therefore, you get this UserWarning: No labeled objects found. Use label='...' kwarg on indivial plots.
        ax2.xaxis_date()
        ax2.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        
        #绘制macd
        ax4.plot(stock_data['diff'],LineWidth=0.5,label='diff')
        ax4.plot(stock_data['dea'],LineWidth=0.5,label='dea')
        ax4.bar(stock_data['macd'].index,stock_data['macd'].values,width= 0.5)
        plt.setp(ax4.get_xticklabels(), visible=False)# 隐藏x轴标签
        ax4.legend()
        ax4.grid(True)
        #绘制成交量
        plt.bar(self.mat_data[:,0], self.mat_data[:,5], width= 0.5)# ? mat_data[:,0] - 0.25
        plt.plot(self.mat_data[:,0], self.mat_data[:,6], LineWidth=0.5,color='r',label='v_ma10')
        plt.legend()
        ax3.grid(True)
    
        
        plt.show() 
    
    #决策函数
    def signal(self,m1 = 'ma5' , m2 = 'ma20'):
        stock_data = self.df
        stock_data[m1+'-'+ m2] = stock_data[m1] - stock_data[m2] #均线高度差
        stock_data['diff'] = np.sign(stock_data[m1+'-'+ m2])# 买卖点
        stock_data['signal'] = np.sign(stock_data['diff'] - stock_data['diff'].shift(1))#注意前后顺序
        stock_data.fillna(0,inplace=True)#填充缺失值
        signals = pd.concat([
            pd.DataFrame({'price':stock_data.loc[stock_data['signal'] == 1 ,'close'],
                          'diff':stock_data.loc[stock_data['signal'] == 1 ,'diff'],
                          'signal':'buy'}),
            pd.DataFrame({'price':stock_data.loc[stock_data['signal'] == -1 ,'close'],
                          'diff':stock_data.loc[stock_data['signal'] == -1 ,'diff'],
                          'signal':'sell'}),
            ])
        signals.sort_index(inplace = True)
        price = signals.loc[(signals['signal'] == 'buy') & (signals['diff']) == 1 ,'price']
        profit = pd.Series(signals["price"] - signals["price"].shift(1)).loc[
                signals.loc[(signals["signal"].shift(1) == "buy") & (signals["diff"].shift(1) == 1)].index].tolist()
        end_date = signals["price"].loc[
                signals.loc[(signals["signal"].shift(1) == "buy") & (signals["diff"].shift(1) == 1)].index].index
        i = min(len(price),len(profit),len(end_date))
        profits = pd.DataFrame({
            'price':price[:i],
            'profit': profit[:i],
            "end date":end_date[:i] 
            })
        tradeperiods =pd.DataFrame({"start":profits.index,
                                    "end":profits["end date"]})
        try:
            print('ddddddddddddddd')
            #注意 x["end"]:x["start"] 前后顺训 从前到后
            profits["low"] =tradeperiods.apply(lambda x: min(stock_data.loc[x["start"]:x["end"],"low"]), axis =1)
            profits["high"] =tradeperiods.apply(lambda x: max(stock_data.loc[x["start"]:x["end"],"high"]), axis =1)
            profits["sell price"] = profits["price"] + profits['profit']
            cols = ['end date','price','low','profit','sell price','high']
            profits = profits[cols]
        except ValueError as e:
            print('xxxxxxxxxxxxxxx')
            print(e)
        finally: 
            
#            stock_data['signal'].plot(ylim=(-2,2))
#            plt.show()           
#            print(stock_data['signal'].value_counts())
            return signals,profits
    #回测收益函数
    def huice_shouyi(self, port_value =.1, batch =100,stoploss =.2):
            _,data = self.signal()
            cash = 10000
            backtest =pd.DataFrame({"Start Port. Value": [],
                                 "End Port. Value": [],
                                 "End Date": [],
                                 "Shares": [],
                                 "Share Price": [],
                                 "Trade Value": [],
                                 "Profit per Share": [],
                                 "Total Profit": [],
                                 "Stop-Loss Triggered": []})
    #        port_value =.1# Max proportion of portfolio bet on any trade
    #        batch =100# Number of shares bought per batch
    #        stoploss =.2# % of trade loss that would trigger a stoploss
            for index, row in data.iterrows():
                batches =np.floor(cash *port_value) //np.ceil(batch *row["price"]) # Maximum number of batches of stocks invested in
                trade_val =batches *batch *row["price"] # How much money is put on the line with each trade
                if row['low'] < (1-stoploss) *row["price"]:   # Account for the stop-loss
                    share_profit = -np.round((stoploss) *row["price"], 2)
                    stop_trig =True
                else:
                    share_profit =row["profit"]
                    stop_trig =False
                profit =share_profit *batches *batch # Compute profits
            # Add a row to the backtest data frame containing the results of the trade
                backtest = backtest.append(pd.DataFrame({
                            "Start Port. Value": cash,
                            "End Port. Value": cash +profit,
                            "End Date": row["end date"],
                            "Shares": batch *batches,
                            "Share Price": row["price"],
                            "Trade Value": trade_val,
                            "Profit per Share": share_profit,
                            "Total Profit": profit,
                            "Stop-Loss Triggered": stop_trig
                        }, index =[index]))
                cash =max(0, cash +profit)
            backtest["End Port. Value"].plot()
            plt.show()
    #        return (backtest["End Port. Value"][-1]-backtest["End Port. Value"][0])
            return backtest


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        