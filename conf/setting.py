# -*- coding: utf-8 -*-

#资金
cash=3000

#仓位
port_value=1.0

#一手股票数量
batch=100

#止损开关
stop_switch=True
#止损点
stoploss=0.1

#股票代码
codes1 = {
        '紫金矿业':'sh.601899',
        '君正集团':'sh.601216',
        '五粮液':'sz.000858',
        '新希望':'sz.000876',
        '比亚迪':'sz.002594'
        }
codes2 = {
        '包钢股份':'sh.600010',
        }

#选择股票代码
codes=codes2
        
#选择应用的决策
strategy='strategy'

#是否绘制回测结果
drawres=False
