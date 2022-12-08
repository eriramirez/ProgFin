#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system(' pip install cvxpy')
get_ipython().system(' pip install riskfolio-lib')
get_ipython().system(' pip install yfinance')


# In[3]:


from datetime import datetime, timedelta
import cvxpy as cp
import riskfolio as rp
import numpy as np
import pandas as pd
import yfinance as yf
import warnings


# In[5]:


warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:.4%}'.format

# Data range
five_years = timedelta(days=365*5, )
end = datetime.now()
start = end - five_years

# Tickers of assets
assets = ['JCI', 'TGT', 'CMCSA', 'CPB', 'MO', 'APA', 
        'MMC', 'JPM', 'ZION', 'PSA', 'BAX', 'BMY', 'LUV', 
        'PCAR', 'TXT', 'TMO', 'DE', 'MSFT', 'HPQ', 'SEE', 
        'VZ', 'CNP', 'NI', 'T', 'BA']
assets.sort()

# Downloading data
data = yf.download(assets, start = start, end = end)
data = data.loc[:,('Adj Close', slice(None))]
data.columns = assets


# In[7]:


#Calculating returns
Y =  data[assets].pct_change().dropna()
display(Y.head())


# In[9]:


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


# In[11]:


# Ploting the composition of the portfolio
ax = rp.plot_pie(w=w, title='Sharpe Mean Variance', others=0.05, nrow=25, cmap='tab20',
                height=6, width=10, ax=None)


# In[12]:


# Calculate de efficient frontier
points = 50 # Number of points in the frontier
frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)
display(frontier.T.head())


# In[14]:


# Plotting the efficient frontier

label = 'Max Risk Adjusted Return Portfolio'
mu = port.mu # Expected returns
cov = port.cov # Covariance matrix
returns = port.returns # Returns of assets

ax = rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=returns, rm=rm, rf=rf, 
                    alpha=0.05, cmap='viridis', w=w, label=label, marker='*', s=16, c='r', 
                    height=6, width=10, ax=None)

