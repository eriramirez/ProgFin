#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Optimization of an International Portfolio


# In[2]:


get_ipython().system(" pip install 'pandas_datareader>=0.10'")


# In[3]:


# Import the necessary libraries 
from pandas_datareader.data import DataReader
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List
import yfinance as yf


# In[4]:


# Create the formula to get the dates of the last 5 years.
def fnct_last_five_years():
    five_years = timedelta(days=365*5, )
    now = datetime.now()
    five_years_ago = now - five_years
    return now, five_years_ago

now, five_years_ago = fnct_last_five_years()
print(now)
print(five_years_ago)


# In[5]:


def fnct_get_ticker_data(ticker: str, data_source: str = "yahoo") -> pd.DataFrame:
    """Get the data in the last 5 years for the specified ticker"""
    print(f'downloading data for {ticker}')
    now, five_years_ago = fnct_last_five_years()
    ticker_df = DataReader(ticker, data_source, five_years_ago, now)
    return ticker_df


def fnct_convert_currency(ticker_adj_close:pd.Series, currency:pd.Series) -> pd.Series:
    df = pd.DataFrame({"x":ticker_adj_close, "c":currency})
    # drop rows where all columns in subset are NA
    df = df.dropna(axis=0, how='all', subset=('x', 'c'))
    # fill with the value of the previous date's values
    df = df.fillna(method='ffill')
    # in case there are empty rows at the beginning, fill with following date's values
    df = df.fillna(method='bfill')
    return df['x'] * df['c']


def fnct_get_currency(*tickers):
    """obtain the currency for each ticker"""
    currencies = dict()
    for ticker in tickers:
        t = yf.Ticker(ticker, )
        currencies[ticker] = t.info["currency"]
    return currencies

def fnct_get_currencies_data(currencies:dict):
    """Use the output of get_currency to read the data for all the currencies once"""
    currencies_data = {}
    unique_currencies = set(currencies.values())
    ticker_map = {
        "USD": "MXN=X",
        "CAD": "CADMXN=X",
        "EUR": "EURMXN=X",
    }
    for c in unique_currencies:
        if c == "MXN":
            continue
        exchange = ticker_map[c]
        currencies_data[c] = fnct_get_ticker_data(exchange)['Close'] # {"USD":pd.Series, CAD:pd.Series}
    df = pd.DataFrame(currencies_data)
    df["MXN"] = 1
    return df

def fnct_get_tickers_in_mxn(currencies:List[str]):
    c_df = fnct_get_currencies_data(currencies)
    t_data = {}
    for ticker, coin in currencies.items():
        t = fnct_get_ticker_data(ticker)['Adj Close']
        t_in_mxn = fnct_convert_currency(t, c_df[coin])
        t_data[ticker] = t_in_mxn
    return pd.DataFrame(t_data)


# In[6]:


def suma(a, b):
    c = a + b
    return(c)

suma(5, 7)


# In[7]:


#tickers = ["BIMBOA.MX", "CEMEXCPO.MX", "PE&OLES.MX", "AMXL.MX", "HERDEZ.MX",
#    "BBD-B.TO", "RY.TO", "ENB.TO", 
#    "VWAGY", "SAP", "NSRGY", "EADSY",]
tickers = ['JCI', 'TGT', 'CMCSA', 'CPB', 'MO', 'APA', 
        'MMC', 'JPM', 'ZION', 'PSA', 'BAX', 'BMY', 'LUV', 
        'PCAR', 'TXT', 'TMO', 'DE', 'MSFT', 'HPQ', 'SEE', 
        'VZ', 'CNP', 'NI', 'T', 'BA']
currencies = fnct_get_currency(*tickers)


# In[8]:


currencies


# In[9]:


data = fnct_get_tickers_in_mxn(currencies)


# In[10]:


data


# In[11]:


pct_change_df = data.pct_change()


# In[12]:


ann_mean_return = ((1 + pct_change_df.mean())**252)-1
print(ann_mean_return)


# In[13]:


ann_stdev = pct_change_df.std() * (252**(1/2))
print(ann_stdev)


# In[14]:


pct_change_df.cov()


# In[15]:


weight = np.full_like(ann_stdev,1/len(ann_stdev))
weight


# In[16]:


portaf_ann_stdev = ((weight @ pct_change_df.cov()) @ weight.T) ** (1/2)
portaf_ann_stdev


# In[17]:


pct_change


# In[ ]:


ticker = 'CADMXN=X'
data_source = 'yahoo'
goog = DataReader(ticker, data_source, five_years_ago, now)
goog


# In[ ]:


ticker = 'CEMEXCPO.MX'
data_source = 'yahoo'
cemex = DataReader(ticker, data_source, five_years_ago, now)


# In[ ]:


ticker = 'MXN=X'
data_source = 'yahoo'
mxn = DataReader(ticker, data_source, five_years_ago, now)


# In[ ]:


df = pd.DataFrame({"goog":goog.Close, "cemex":cemex.Close, 'mxn':mxn['Close']})
# drop rows where all columns in subset are NA
df = df.dropna(axis=0, how='all', subset=('goog', 'cemex'))
# fill with the value of the previous date's values
df = df.fillna(method='ffill')
# in case there are empty rows at the beginning, fill with following date's values
df = df.fillna(method='bfill')


# In[ ]:


#Add a column with google prices in MXN
df['goog_mxn'] = df.goog * df.mxn


# In[ ]:


df.plot(y=['goog_mxn', "cemex"])


# In[ ]:


df.corr()


# In[ ]:


df.cov()


# In[ ]:


df.std()


# In[ ]:


df.std() * np.sqrt(252)


# In[ ]:


df['goog_mxn_change'] = df.goog_mxn.pct_change()


# In[ ]:


df.to_excel('example.xlsx')


# In[ ]:




