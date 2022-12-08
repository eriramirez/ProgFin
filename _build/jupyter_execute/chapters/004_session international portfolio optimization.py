#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Optimization of an International Portfolio


# In[2]:


get_ipython().system(" pip install 'pandas_datareader>=0.10'")
get_ipython().system(' pip install cvxpy')
get_ipython().system(' pip install riskfolio-lib')
get_ipython().system(' pip install yfinance')


# In[7]:


# Import the necessary libraries 
from pandas_datareader.data import DataReader
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List
import yfinance as yf
import cvxpy as cp
import riskfolio as rp
import warnings


# In[8]:


# Create the formula to get the dates of the last 5 years.
def fnct_last_five_years():
    five_years = timedelta(days=365*5, )
    now = datetime.now()
    five_years_ago = now - five_years
    return now, five_years_ago

now, five_years_ago = fnct_last_five_years()
print(now)
print(five_years_ago)


# In[9]:


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


# In[10]:


def suma(a, b):
    c = a + b
    return(c)

suma(5, 7)


# In[11]:


#tickers = ["BIMBOA.MX", "CEMEXCPO.MX", "PE&OLES.MX", "AMXL.MX", "HERDEZ.MX",
#    "BBD-B.TO", "RY.TO", "ENB.TO", 
#    "VWAGY", "SAP", "NSRGY", "EADSY",]
assets = ['JCI', 'TGT', 'CMCSA', 'CPB', 'MO', 'APA', 
        'MMC', 'JPM', 'ZION', 'PSA', 'BAX', 'BMY', 'LUV', 
        'PCAR', 'TXT', 'TMO', 'DE', 'MSFT', 'HPQ', 'SEE', 
        'VZ', 'CNP', 'NI', 'T', 'BA']
currencies = fnct_get_currency(*assets)


# In[12]:


currencies


# In[13]:


data = fnct_get_tickers_in_mxn(currencies)


# In[14]:


data


# In[15]:


data.columns = assets
Y =  data[assets].pct_change().dropna()
display(Y.head())
#pct_change_df = data.pct_change()


# In[16]:


# Building the portfolio object
port = rp.Portfolio(returns = Y)

#Calculating optimal portfolio

#Select method and estimate input parameters
method_mu = 'hist' # method to estimate expected returns based on historical data
method_cov = 'hist' # method to estimate covariance matrix based on historical data 

port.assets_stats(method_mu = method_mu, method_cov = method_cov, d = 0.94)

#Estimate optimal portfolio
model = "Classic" # Could be Classic (historical), BL (Black Litterman), or FM (FActor Model)
rm = "MV" # Risk measure used, this time will be variance
obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility of Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk Free Rate
l = 0 # Risk aversion factor, unly useful when objective is 'Utility'

w = port.optimization(model=model, obj=obj, rf=rf, l=l, hist=hist)

display(w.T)


# In[34]:


rp.Reports.jupyter_report(Y, w)


# In[35]:


rp.Reports.excel_report(
    Y,
    w,
    rf=0,
    alpha=0.05,
    t_factor=252,
    ini_days=1,
    days_per_year=252,
    name=r"C:\Users\L00616607\Developer\ProgFin\python port1.xlsx",
)


# In[17]:


# Ploting the composition of the portfolio
ax = rp.plot_pie(w=w, title='Sharpe Mean Variance', others=0.05, nrow=len(data.columns), 
                cmap='tab20', height=6, width=10, ax=None)


# In[19]:


ann_mean_return = ((1 + Y.mean())**252)-1
print(ann_mean_return)


# In[20]:


ann_stdev = Y.std() * (252**(1/2))
print(ann_stdev)


# In[23]:


Y.cov()


# In[31]:


w.round(4)


# In[ ]:


#weight = np.full_like(ann_stdev,1/len(ann_stdev))
#weight


# In[28]:


portaf_ann_stdev = ((w.T @ Y.cov()) @ w) ** (1/2)
portaf_ann_stdev


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




