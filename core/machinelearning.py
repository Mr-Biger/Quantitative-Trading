# -*- coding: utf-8 -*-
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from math import log
import numpy as np
import operator
   
#计算香浓熵
class CalcShannonEnt():
    #初始化函数
    def __init__(self,df):
        
        self.df = df
        dataSet, features = self.createDataSet()
        print("最优特征索引值:" + str(self.chooseBestFeatureToSplit(dataSet)) + features[int(self.chooseBestFeatureToSplit(dataSet))])
        featLabels = []
        myTree = self.createTree(dataSet, features, featLabels)
        print(myTree)
        self.createPlot(myTree)

    def calcShannonEnt(self,dataSet):
        
        """
        函数说明:计算给定数据集的经验熵(香农熵)
        
        参数说明：
            dataSet - 数据集
        返回值说明:
            shannonEnt - 经验熵(香农熵)

        """
        
        numEntires = len(dataSet)                        #返回数据集的行数
        labelCounts = {}                                #保存每个标签(Label)出现次数的字典
        for featVec in dataSet:                            #对每组特征向量进行统计
            currentLabel = featVec[-1]                    #提取标签(Label)信息
            if currentLabel not in labelCounts.keys():    #如果标签(Label)没有放入统计次数的字典,添加进去
                labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1                #Label计数
        shannonEnt = 0.0                                #经验熵(香农熵)
        for key in labelCounts:                            #计算香农熵
            prob = float(labelCounts[key]) / numEntires    #选择该标签(Label)的概率
            shannonEnt -= prob * log(prob, 2)            #利用公式计算
        return shannonEnt                                #返回经验熵(香农熵)
    #创建数据集 及 标签集
    def createDataSet(self):
        #data= GetStockData().pd_data
        data = self.df.dropna()
        data['sing'] = np.sign(data['close'] - data['close'].shift(-1))#计算涨跌
        #del data['code']
        data = data.dropna()
        dataSet = data.as_matrix().tolist()
        ####################################################
        #labels = ['open','close','high','low','volume','ma3','ma5','ma10','ma20','ma30','ma60','sing']
        labels =  data.columns.tolist() #创建标签
        
        return dataSet,labels
    #按照给定特征划分数据集
    def splitDataSet(self,dataSet, axis, value):   
        """
        函数说明:按照给定特征划分数据集
        
        Parameters:
            dataSet - 待划分的数据集
            axis - 划分数据集的特征
            value - 需要返回的特征的值
        Returns:
            无
        Author:
            Jack Cui
        Modify:
            2017-03-30
        """
        retDataSet = []                                        #创建返回的数据集列表
        for featVec in dataSet:                             #遍历数据集
            if featVec[axis] == value:
                reducedFeatVec = featVec[:axis]                #去掉axis特征
                reducedFeatVec.extend(featVec[axis+1:])     #将符合条件的添加到返回的数据集
                retDataSet.append(reducedFeatVec)
        return retDataSet                                      #返回划分后的数据集
    
    #选择最优特征
    def chooseBestFeatureToSplit(self,dataSet):
        """
        函数说明:选择最优特征
        
        Parameters:
            dataSet - 数据集
        Returns:
            bestFeature - 信息增益最大的(最优)特征的索引值
        Author:
            Jack Cui
        Modify:
            2017-03-30
        """
        numFeatures = len(dataSet[0]) - 1                    #特征数量
        baseEntropy = self.calcShannonEnt(dataSet)                 #计算数据集的香农熵
        bestInfoGain = 0.0                                  #信息增益
        bestFeature = -1                                    #最优特征的索引值
        for i in range(numFeatures):                         #遍历所有特征
            #获取dataSet的第i个所有特征
            featList = [example[i] for example in dataSet]
            uniqueVals = set(featList)                         #创建set集合{},元素不可重复
            newEntropy = 0.0                                  #经验条件熵
            for value in uniqueVals:                         #计算信息增益
                subDataSet = self.splitDataSet(dataSet, i, value)         #subDataSet划分后的子集
                prob = len(subDataSet) / float(len(dataSet))           #计算子集的概率
                newEntropy += prob * self.calcShannonEnt(subDataSet)     #根据公式计算经验条件熵
            infoGain = baseEntropy - newEntropy                     #信息增益
            print("第%d个特征的增益为%.3f" % (i, infoGain))            #打印每个特征的信息增益
            if (infoGain > bestInfoGain):                             #计算信息增益
                bestInfoGain = infoGain                             #更新信息增益，找到最大的信息增益
                bestFeature = i                                     #记录信息增益最大的特征的索引值
        return bestFeature                                             #返回信息增益最大的特征的索引值
    #统计classList中出现此处最多的元素(类标签)
    def majorityCnt(self, classList):
        """
        函数说明:统计classList中出现此处最多的元素(类标签)

        Parameters:
            classList - 类标签列表
        Returns:
            sortedClassCount[0][0] - 出现此处最多的元素(类标签)
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        classCount = {}
        for vote in classList:                                        #统计classList中每个元素出现的次数
            if vote not in classCount.keys():classCount[vote] = 0   
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)        #根据字典的值降序排序
        return sortedClassCount[0][0]    #返回classList中出现次数最多的元素
    
    #创建决策树
    def createTree(self, dataSet, labels, featLabels):
        """
        函数说明:创建决策树

        Parameters:
            dataSet - 训练数据集
            labels - 分类属性标签
            featLabels - 存储选择的最优特征标签
        Returns:
            myTree - 决策树
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-25
        """
        classList = [example[-1] for example in dataSet]            #取分类标签(是否放贷:yes or no)
        if classList.count(classList[0]) == len(classList):            #如果类别完全相同则停止继续划分
            return classList[0]
        if len(dataSet[0]) == 1:                                    #遍历完所有特征时返回出现次数最多的类标签
            return self.majorityCnt(classList)
        bestFeat = self.chooseBestFeatureToSplit(dataSet)                #选择最优特征
        bestFeatLabel = labels[bestFeat]                            #最优特征的标签
        featLabels.append(bestFeatLabel)
        myTree = {bestFeatLabel:{}}                                    #根据最优特征的标签生成树
        del(labels[bestFeat])                                        #删除已经使用特征标签
        featValues = [example[bestFeat] for example in dataSet]        #得到训练集中所有最优特征的属性值
        uniqueVals = set(featValues)                                #去掉重复的属性值
        for value in uniqueVals:                                    #遍历特征，创建决策树。                       
            myTree[bestFeatLabel][value] = self.createTree(self.splitDataSet(dataSet, bestFeat, value), labels, featLabels)
        return myTree
    #获取决策树叶子结点的数目    
    def getNumLeafs(self, myTree):
        """
        函数说明:获取决策树叶子结点的数目

        Parameters:
            myTree - 决策树
        Returns:
            numLeafs - 决策树的叶子结点的数目
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        numLeafs = 0                                                #初始化叶子
        firstStr = next(iter(myTree))                                #python3中myTree.keys()返回的是dict_keys,不在是list,所以不能使用myTree.keys()[0]的方法获取结点属性，可以使用list(myTree.keys())[0]
        secondDict = myTree[firstStr]                                #获取下一组字典
        for key in secondDict.keys():
            if type(secondDict[key]).__name__=='dict':                #测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
                numLeafs += self.getNumLeafs(secondDict[key])
            else:   numLeafs +=1
        return numLeafs

    #获取决策树的层数
    def getTreeDepth(self, myTree):
        """
        函数说明:获取决策树的层数

        Parameters:
            myTree - 决策树
        Returns:
            maxDepth - 决策树的层数
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        maxDepth = 0                                                #初始化决策树深度
        firstStr = next(iter(myTree))                                #python3中myTree.keys()返回的是dict_keys,不在是list,所以不能使用myTree.keys()[0]的方法获取结点属性，可以使用list(myTree.keys())[0]
        secondDict = myTree[firstStr]                                #获取下一个字典
        for key in secondDict.keys():
            if type(secondDict[key]).__name__=='dict':                #测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
                thisDepth = 1 + self.getTreeDepth(secondDict[key])
            else:   thisDepth = 1
            if thisDepth > maxDepth: maxDepth = thisDepth            #更新层数
        return maxDepth
    #绘制结点
    def plotNode(self, nodeTxt, centerPt, parentPt, nodeType):
        """
        函数说明:绘制结点

        Parameters:
            nodeTxt - 结点名
            centerPt - 文本位置
            parentPt - 标注的箭头位置
            nodeType - 结点格式
        Returns:
            无
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        arrow_args = dict(arrowstyle="<-")                                            #定义箭头格式
        font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)        #设置中文字体
        self.createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',    #绘制结点
            xytext=centerPt, textcoords='axes fraction',
            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args, FontProperties=font)

    #标注有向边属性值
    def plotMidText(self, cntrPt, parentPt, txtString):
        """
        函数说明:标注有向边属性值

        Parameters:
            cntrPt、parentPt - 用于计算标注位置
            txtString - 标注的内容
        Returns:
            无
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]                                            #计算标注位置                   
        yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
        self.createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

    #绘制决策树
    def plotTree(self, myTree, parentPt, nodeTxt):
        """
        函数说明:绘制决策树

        Parameters:
            myTree - 决策树(字典)
            parentPt - 标注的内容
            nodeTxt - 结点名
        Returns:
            无
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        decisionNode = dict(boxstyle="sawtooth", fc="0.8")                                        #设置结点格式
        leafNode = dict(boxstyle="round4", fc="0.8")                                            #设置叶结点格式
        numLeafs = self.getNumLeafs(myTree)                                                          #获取决策树叶结点数目，决定了树的宽度
        depth = self.getTreeDepth(myTree)                                                            #获取决策树层数
        firstStr = next(iter(myTree))                                                            #下个字典                                                 
        cntrPt = (self.plotTree.xOff + (1.0 + float(numLeafs))/2.0/self.plotTree.totalW, self.plotTree.yOff)    #中心位置
        self.plotMidText(cntrPt, parentPt, nodeTxt)                                                    #标注有向边属性值
        self.plotNode(firstStr, cntrPt, parentPt, decisionNode)                                        #绘制结点
        secondDict = myTree[firstStr]                                                            #下一个字典，也就是继续绘制子结点
        self.plotTree.yOff = self.plotTree.yOff - 1.0/self.plotTree.totalD                                        #y偏移
        for key in secondDict.keys():                               
            if type(secondDict[key]).__name__=='dict':                                            #测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
                self.plotTree(secondDict[key],cntrPt,str(key))                                        #不是叶结点，递归调用继续绘制
            else:                                                                                #如果是叶结点，绘制叶结点，并标注有向边属性值                                             
                self.plotTree.xOff = self.plotTree.xOff + 1.0/self.plotTree.totalW
                self.plotNode(secondDict[key], (self.plotTree.xOff, self.plotTree.yOff), cntrPt, leafNode)
                self.plotMidText((self.plotTree.xOff, self.plotTree.yOff), cntrPt, str(key))
        self.plotTree.yOff = self.plotTree.yOff + 1.0/self.plotTree.totalD

    #创建绘制面板
    def createPlot(self, inTree):
        """
        函数说明:创建绘制面板

        Parameters:
            inTree - 决策树(字典)
        Returns:
            无
        Author:
            Jack Cui
        Blog:
            http://blog.csdn.net/c406495762
        Modify:
            2017-07-24
        """
        fig = plt.figure(1, facecolor='white')                                                    #创建fig
        fig.clf()                                                                                #清空fig
        axprops = dict(xticks=[], yticks=[])
        ax1 = plt.subplot(111, frameon=False, **axprops)                                #去掉x、y轴
        self.plotTree.totalW = float(self.getNumLeafs(inTree))                                            #获取决策树叶结点数目
        self.plotTree.totalD = float(self.getTreeDepth(inTree))                                            #获取决策树层数
        self.plotTree.xOff = -0.5/self.plotTree.totalW; self.plotTree.yOff = 1.0;                                #x偏移
        self.plotTree(inTree, (0.5,1.0), '')                                                            #绘制决策树
        plt.show()


#计算K临近
class KNeighbors():
    #初始化函数
    def __init__(self,df):
        self.df = df
        self.datingClassTest()
    
    #创建数据集 及 标签集
    def createDataSet(self):
        #data= GetStockData().pd_data
        data = self.df.dropna()
        data['sing'] = -np.sign(data['close'] - data['close'].shift(1))
        #del data['code']
        data = data.dropna()
        returnMat = data.as_matrix()
        print(data)

        classLabelVector = data['sing'].tolist()#预测1天后的升降
        
        return returnMat,classLabelVector
    
    #函数说明:kNN算法,分类器
    def classify0(self, inX, dataSet, labels, k):
        """        
        Parameters:
            inX - 用于分类的数据(测试集)
            dataSet - 用于训练的数据(训练集)
            labes - 分类标签
            k - kNN算法参数,选择距离最小的k个点
        Returns:
            sortedClassCount[0][0] - 分类结果returnMat = data[:,4:9]
        
        Modify:
            2017-03-24
        """
        #numpy函数shape[0]返回dataSet的行数
        dataSetSize = dataSet.shape[0]
        #在列向量方向上重复inX共1次(横向),行向量方向上重复inX共dataSetSize次(纵向)
        diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
        #二维特征相减后平方
        sqDiffMat = diffMat**2
        #sum()所有元素相加,sum(0)列相加,sum(1)行相加
        sqDistances = sqDiffMat.sum(axis=1)
        #开方,计算出距离
        distances = sqDistances**0.5
        #返回distances中元素从小到大排序后的索引值
        sortedDistIndices = distances.argsort()
        #定一个记录类别次数的字典
        classCount = {}
        for i in range(k):
            #取出前k个元素的类别
            voteIlabel = labels[sortedDistIndices[i]]
            #dict.get(key,default=None),字典的get()方法,返回指定键的值,如果值不在字典中返回默认值。
            #计算类别次数
            classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        #python3中用items()替换python2中的iteritems()
        #key=operator.itemgetter(1)根据字典的值进行排序
        #key=operator.itemgetter(0)根据字典的键进行排序
        #reverse降序排序字典
        sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
        #返回次数最多的类别,即所要分类的类别
        return sortedClassCount[0][0]
    
    #函数说明:对数据进行归一化
    def autoNorm(self, dataSet):
        """       
        Parameters:
            dataSet - 特征矩阵
        Returns:
            normDataSet - 归一化后的特征矩阵
            ranges - 数据范围
            minVals - 数据最小值
        
        Modify:
            2017-03-24
        """
        #获得数据的最小值
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        #最大值和最小值的范围
        ranges = maxVals - minVals
        #shape(dataSet)返回dataSet的矩阵行列数
        normDataSet = np.zeros(np.shape(dataSet))
        #返回dataSet的行数
        m = dataSet.shape[0]
        #原始值减去最小值
        normDataSet = dataSet - np.tile(minVals, (m, 1))
        #除以最大和最小值的差,得到归一化数据
        normDataSet = normDataSet / np.tile(ranges, (m, 1))
        #返回归一化数据结果,数据范围,最小值
        return normDataSet, ranges, minVals
    
    #函数说明:分类器测试函数
    def datingClassTest(self):
        """       
        Parameters:
            无
        Returns:
            normDataSet - 归一化后的特征矩阵
            ranges - 数据范围
            minVals - 数据最小值
        
        Modify:
            2017-03-24
        """
    
        datingDataMat, datingLabels = self.createDataSet()
        #取所有数据的百分之十
        hoRatio = 0.10
        #数据归一化,返回归一化后的矩阵,数据范围,数据最小值
        normMat, ranges, minVals = self.autoNorm(datingDataMat)
        #获得normMat的行数
        m = normMat.shape[0]
        #百分之十的测试数据的个数
        numTestVecs = int(m * hoRatio)
        #分类错误计数
        errorCount = 0.0
    
        for i in range(numTestVecs):
            #前numTestVecs个数据作为测试集,后m-numTestVecs个数据作为训练集
            classifierResult = self.classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], 4)
            print("分类结果:%d\t真实类别:%d" % (classifierResult, datingLabels[i]))
            if classifierResult != datingLabels[i]:
                errorCount += 1.0
        print("错误率:%f%%" %(errorCount/float(numTestVecs)*100))