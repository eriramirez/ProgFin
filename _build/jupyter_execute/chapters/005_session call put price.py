#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pandas_datareader.data as wb
from scipy.stats import norm

my_volat = .28
my_time = 0.75  
my_excercise_price = 40
my_market_price = 43.5
my_rf_rate = .085

def d1(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time) :
    return (np.log(my_market_price/my_excercise_price) + ((my_rf_rate + my_volat**2)/2)*my_time) / (my_volat * np.sqrt(my_time))

def d2(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time) :
    return (np.log(my_market_price/my_excercise_price) + ((my_rf_rate - my_volat**2)/2)*my_time) / (my_volat * np.sqrt(my_time))

def call(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time) :
    d_uno = d1(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time)
    d_dos = d2(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time)
    return (my_market_price*norm.cdf(d_uno)) - (my_excercise_price*np.exp(-my_rf_rate*my_time)*norm.cdf(d_dos))

def put(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time) :
    d_uno = d1(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time)
    d_dos = d2(my_market_price, my_excercise_price, my_rf_rate, my_volat, my_time)
    return ((my_excercise_price*np.exp(-my_rf_rate*my_time)*norm.cdf(-d_dos)) - (my_market_price*norm.cdf(-d_uno)))

call_price = call(
    my_market_price,
    my_excercise_price,
    my_rf_rate,
    my_volat,
    my_time
)

put_price = put(
    my_market_price,
    my_excercise_price,
    my_rf_rate,
    my_volat,
    my_time
)
print(f"Precio Call: {call_price:.4f}")
print(f"Precio Put: {put_price:.4f}")



# In[ ]:




