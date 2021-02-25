# Quantitative-Trading
目录组织方式

investor/
|-- script/    存放项目的一些可执行文件
|   |-- __init__
|   |-- start.py   启动程序
|
|-- core/   存放项目的所有核心代码,程序的入口为main.py。
|   |-- tests/   存放单元测试代码
|   |   |-- __init__.py
|   |   |-- test.main.py  
|   |
|   |-- __init__.py
|   |-- main.py          入口模块
|   |-- datacenter.py     存储数据模块
|   |-- stragegy.py       股票指标计算 数据分析 回测模块
|   |-- stragety_doc.py   策略模块
|   |-- drawstockdata.py  绘图模块
|   |-- machinelearing.py 机器学习模块
|   |-- classicalmodel.py 经典模型模块
|
|-- conf/    配置文件
|   |-- __init__.py
|   |-- setting.py   写上相关配置
|
|---db/    数据库文件
|   |-- db.json    写数据库文件
|   
|-- docs/   存放一些文档
|   
|-- lib/   库文件，放自定义模块和包
|   |-- __init__.py
|   |-- common.py    放常用的功能
|
|-- log/   日志文件
|   |-- access.log    写上日志
|
|-- __init__.py
|-- README    项目说明文件

注：运行程序时，在script目录下执行start.py代码，不可以直接执行core下的模块。
###########################
命名规则：
股票历史数据 - hist_data
股票分析数据 - df
收益率 - yield_rate
