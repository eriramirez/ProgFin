#!/usr/bin/env python
# coding: utf-8

# # Coding first examples

# In[1]:


# Generate the first n numbers of the fibonacci series
n = 30
fbci = [0, 1]
for _ in range(2, n):
    fbci.append(fbci[-1] + fbci[-2])
print(fbci)


# In[2]:


for _ in range(20):
    print(_)

