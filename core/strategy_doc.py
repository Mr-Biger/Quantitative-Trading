# -*- coding: utf-8 -*-

#决策

strategies={}

strategies['strategy0'] = {
    'anal_macd':{
        'buy':"self.df['trend_sign'][i]==-1, self.df['distance_sign'][i]==-1, self.df['cross'][i]==0",
        'sell':"self.df['trend_sign'][i]==1, self.df['distance_sign'][i]==1, self.df['cross'][i]==0"
        },
    'anal_kdj':{
        }
    }

strategies['strategy1'] = {
    'anal_macd':{
        'buy':"self.df['trend_sign_macd'][i]==-1, self.df['distance_sign_macd'][i]==-1, self.df['cross_macd'][i]==0 ",
        'sell':"self.df['trend_sign_macd'][i]==1, self.df['distance_sign_macd'][i]==1, self.df['cross_macd'][i]==0 "
        },
    'anal_kdj':{
        'buy':",self.df['KDJ_K'][i]<=20, self.df['KDJ_D'][i]<=20, self.df['KDJ_J'][i]<=20",
        'sell':",self.df['KDJ_K'][i]>=80, self.df['KDJ_D'][i]>=80, self.df['KDJ_J'][i]>=80"
        }
    }
        
strategies['strategy2'] = {
    'anal_macd':{
        'buy':"self.df['cross_macd'][i]==2",
        'sell':"self.df['cross_macd'][i]==-2"
        }
    }

strategies['strategy3'] = {
    'anal_momentum':{
        'buy':"self.df['momentum'][i]>0",
        'sell':"self.df['momentum'][i]<0"
        }   
    }

strategies['strategy'] = {
    'anal_rsi':{
        'buy':"self.df['cross_rsi'][i]==2",
        'sell':"self.df['cross_rsi'][i]==-2"
        }
    }

