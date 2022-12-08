#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')


# In[2]:


get_ipython().system(' pip install pandas_datareader')


# In[3]:


import yfinance as yf
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


# In[ ]:





# In[5]:


# Get currency
def get_currency (*tickers):  # obtain the currency for each ticker
    currencies = dict()
    for ticker in tickers :
        t = yf.Ticker(ticker)
        currencies[ticker] = t.info["currency"]
    return currencies
get_currency("GOOG", "GCC.MX")


# In[6]:


# Get tickers
def get_tickers(*tickers): 
    for ticker in tickers :
        
        # retrieve data (como la sesión 003)
        # revisar el tipo de cambio con yfinance de cada ticker
        # hacer un for loop para unificar las acciones que tienen el mismo tipo de cambio

# crear un diccionario ( collections defaultdict )


# In[ ]:


# Get Close Price for each ticker
def get_close_price(*tickers) :
    for 

