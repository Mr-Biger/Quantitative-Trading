# -*- coding: utf-8 -*-

from scipy import linalg
import matplotlib.pyplot as plt
import numpy as np
import ffn
class MeanVariance:
    #定义构造器 传入收益率数据
    def __init__(self, returns):
        self.returns = returns
    #定义最小化方差函数，即求解二次规划    
    def minVar(self, goalRet):
        #计算协方差
        covs = np.array(self.returns.cov())
        #计算均值
        means = np.array(self.returns.mean())
        L1 = np.append(np.append(covs.swapaxes(0,1),[means],0),
                       [np.ones(len(means))],0).swapaxes(0,1)
        
        L2 = list(np.ones(len(means)))
        L2.extend([0,0])
        L3=list(means)
        L3.extend([0,0])
        L4=np.array([L2,L3])
        L=np.append(L1,L4,0)
        results = linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],0))
        return(np.array([list(self.returns.columns),results[:-2]]))
    #定义绘制最小方差前缘曲线函数
    @property
    def frontierCurve(self):
        goals=[x/500000 for x in range(-100,4000)]
        variances=list(map(lambda x: self.calVar(self.minVar(x)[1,:].astype(np.float)),goals))
        plt.plot(variances,goals)
    #给定资产比例，计算收益率均值
    def meanRet(self,fracs):
        meanRisky=ffn.to_returns(self.returns).mean()
        assert len(meanRisky)==len(fracs),'Length of fractions must be equal to number of assets'
        return (np.sum(np.multiply(meanRisky,np.array(fracs))))
    #给定资产比例，计算收益率方差
    def calVar(self, fracs):
        return (np.dot(np.dot(fracs, self.returns.cov()),fracs))
    
    def testModels(self, train_set, test_set, goal_returns):
        pass
    
        
        