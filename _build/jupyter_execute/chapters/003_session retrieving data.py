#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Portfolio Optimization


# In[2]:


get_ipython().system(' pip install pandas_datareader')


# In[3]:


# import the necessary libraries 
from pandas_datareader.data import DataReader
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


# In[4]:


#create the formula to get the dates of the last 5 years.
five_years = timedelta(days=365*5, )
now = datetime.now()
five_years_ago = now - five_years
print(now)
print(five_years_ago)


# In[5]:


ticker = 'GOOG'
data_source = 'yahoo'
goog = DataReader(ticker, data_source, five_years_ago, now)


# In[6]:


ticker = 'CEMEXCPO.MX'
data_source = 'yahoo'
cemex = DataReader(ticker, data_source, five_years_ago, now)


# In[7]:


ticker = 'MXN=X'
data_source = 'yahoo'
mxn = DataReader(ticker, data_source, five_years_ago, now)


# In[8]:


df = pd.DataFrame({"goog":goog.Close, "cemex":cemex.Close, 'mxn':mxn['Close']})
# drop rows where all columns in subset are NA
df = df.dropna(axis=0, how='all', subset=('goog', 'cemex'))
# fill with the value of the previous date's values
df = df.fillna(method='ffill')
# in case there are empty rows at the beginning, fill with following date's values
df = df.fillna(method='bfill')


# In[9]:


#Add a column with google prices in MXN
df['goog_mxn'] = df.goog * df.mxn


# In[10]:


df.plot(y=['goog_mxn', "cemex"])


# In[45]:


df.corr()


# In[46]:


df.cov()


# In[47]:


df.std()


# In[49]:


df.std() * np.sqrt(252)


# In[53]:


df['goog_mxn_change'] = df.goog_mxn.pct_change()


# In[59]:


df.to_excel('example.xlsx')


# In[ ]:




