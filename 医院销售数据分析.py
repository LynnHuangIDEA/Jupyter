#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# In[5]:


data=pd.read_excel("ZYsales2018.xls",dtype="object")


# In[6]:


dataDF=pd.DataFrame(data)


# In[7]:


dataDF.head()


# In[8]:


dataDF.shape


# In[9]:


dataDF.index


# In[10]:


dataDF.columns


# In[11]:


dataDF.count()


# In[12]:


# 使用 rename 函数，把“购药时间”改为“销售时间”
dataDF.rename(columns={"购药时间":"销售时间"},inplace=True)
dataDF.columns


# In[13]:


dataDF.shape


# In[14]:


dataDF = dataDF.dropna()


# In[15]:


dataDF.shape


# In[16]:


dataDF["销售数量"] = dataDF["销售数量"].astype("f8")
dataDF["应收金额"] = dataDF["应收金额"].astype("f8")
dataDF["实收金额"] = dataDF["实收金额"].astype("f8")
dataDF.dtypes


# In[18]:


#定义函数将星期去除
def splitsaletime(timeColser):
    timelist = []
    for t in timeColser:
        timelist.append(t.split(" ")[0]) #[0]表示切割完后选取第一个分片
    timeser = pd.Series(timelist) #将列表转行为一维数据 Series 类型
    return timeser


# In[19]:


# 获取"销售时间"这一列数据
t = dataDF.loc[:,"销售时间"] 
#调用函数去除星期，获取日期
timeser = splitsaletime(t)
# 修改"销售时间" 这一列日期
dataDF.loc[:,"销售时间"] = timeser
dataDF.head()


# In[20]:


#字符串转日期
# errors='coerce' 如果原始数据不符合日期的格式，转换后的值为 NaT
dataDF.loc[:,"销售时间"]=pd.to_datetime(dataDF.loc[:,"销售时间"],errors="coerce")
dataDF.dtypes


# In[21]:


#　转换日期过程中不符合日期格式的数值会被转换为空值 None
#  删除为空的行
dataDF = dataDF.dropna()
dataDF.shape


# In[22]:


# 按销售时间进行升序排序
dataDF = dataDF.sort_values(by="销售时间",ascending=True)
dataDF.head()


# In[23]:


#重置索引 (index)
dataDF = dataDF.reset_index(drop=True)
dataDF.head()


# In[24]:


#查看描述统计信息
dataDF.describe()


# In[25]:


#将 "销售数量" 这一行中小于 0 的数排除掉
pop = dataDF.loc[:,"销售数量"] >0 
dataDF = dataDF.loc[pop,:]


# In[26]:


# 排除异常值后再次查看描述统计信息
dataDF.describe()


# ### 业务指标1 ： 月均消费次数
# 月均消费次数 = 总消费次数 / 月份数 

# In[29]:


#计算总消费次数
# 删除重复数据
kpi1_Df = dataDF.drop_duplicates(subset = ['销售时间','社保卡号'])


# In[31]:


# 有多少行
totall= kpi1_Df.shape[0]
print ('总消费次数： ',totall)


# In[32]:


#计算月份数
# 按销售时间升序排序
kpi1_Df = kpi1_Df.sort_values(by='销售时间',ascending=True)


# In[33]:


kpi1_Df = kpi1_Df.reset_index(drop = True)


# In[34]:


# 获取时间范围
# 最小时间值
startTime = kpi1_Df.loc[0,'销售时间']
# 最大时间值
endTime = kpi1_Df.loc[totall - 1,'销售时间']


# In[35]:


#计算天数
daysI = (endTime - startTime).days


# In[39]:


#月份数， // 表示取整除，返回商的整数部分
monthsI = daysI // 30
print('月份数：',monthsI)


# In[40]:


#计算月均消费次数
kpi1_I = totall // monthsI
print('业务指标1：月均消费次数=', kpi1_I)


# ### 业务指标2：月均消费金额
# 月均消费金额 = 总消费金额 / 月份数

# In[41]:


# 总消费金额
totalMoneyF = dataDF.loc[:,'实收金额'].sum()


# In[42]:


# 月均消费金额
monthMoneyF = totalMoneyF / monthsI
print ('业务指标2：月均消费金额=', monthMoneyF)


# ### 业务指标3：客单价
# 客单价 = 总消费金额 / 总消费次数

# In[43]:


pct = totalMoneyF / totall
print ('业务指标3：客单价=',pct)


# ### 业务指标4：消费趋势

# In[45]:


import matplotlib.pyplot as plt

# 画图用于显示中文字符
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  ## 黑体字体


# In[47]:


# 在操作之前先复制一份数据，防止影响清洗后的数据
groupDf = dataDF


# In[48]:


# 分析每天的消费金额
groupDf.index = groupDf['销售时间']
groupDf.head()


# In[50]:


# 画图
plt.plot(groupDf['实收金额'])
plt.title('按天消费金额图')
plt.xlabel('时间')
plt.ylabel('实收金额')
plt.savefig('./day.png')


# In[51]:


# 分析每月的消费金额
# 将销售时间聚合按月分组
gb = groupDf.groupby(groupDf.index.month)
gb


# In[53]:


# 应用函数，计算每个月的消费总额
monthDf = gb.sum()
monthDf


# In[55]:


# 描绘按月消费金额图
plt.plot(monthDf['实收金额'])
plt.title('按月消费金额图')
plt.xlabel('月份')
plt.ylabel('实收金额')
plt.savefig('./month.png')


# In[58]:


# 分析药品销售情况
# 聚合统计各种药品的销售数量
medicine = groupDf[['商品名称','销售数量']]
bk = medicine.groupby('商品名称')[['销售数量']]
re_medicine = bk.sum()


# In[61]:


# 对药品销售数量按降序排序
re_medicine = re_medicine.sort_values(by='销售数量',ascending=False)
re_medicine.head()


# In[62]:


# 截取销售数量最多的十种药品
top_medicine = re_medicine.iloc[:10,:]
top_medicine


# In[68]:


# 用条形图展示销售数量前十的药品
top_medicine.plot(kind='bar')
plt.title('药品销售前十情况')
plt.xlabel('药品种类')
plt.ylabel('销售数量')
plt.legend(loc=0)
plt.savefig('./medicine.png')


# In[ ]:





# In[ ]:




