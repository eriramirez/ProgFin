#!/usr/bin/env python
# coding: utf-8

# # Time Value Of Money
# The Buy vs Rent Decision

# ## Inputs for determining the amount of the Loan

# In[1]:


# Loan amount (loan):
property_price = 600000
down_payment = .20
loan = house_price*(1-down_payment)
print(f"The loan is valued at {loan:4.2f} USD")


# ## Inputs for determining the monthly interest rate

# In[27]:


# Monthly effective interest rate (i):
ann_interest = .04
#number of months in the capitalization period:
compound_periods = 6
# get effective monthly interest:
i = ((1 + (ann_interest / 12 * compound_periods))**(1 / compound_periods)) - 1
print(f"The monthly efective rate is {i * 100:4.4f} percent")


# ## Inputs for determining the loan life in months

# In[29]:


# Get the loan life in months
years = 25
n = years *12
print(f"The credit will be paid in{n:4.0f} months")


# ##  Financing information
# ### Obtain the monthly payment

# In[31]:


def fnct_pmt(loan, i, n):
    pmt = loan * i *(1 + i)**n / ((1 + i)**n - 1)
    return pmt
    
print(fnct_pmt(loan, i, n))


# ## Inputs for determining the opportunity cost

# In[36]:


# Monthly opportunity Cost from initial disbursment due to the withdrawal from own invested resources:
legal_costs = .00 #as percent of the property price
buying_tax = .03 #as percent of the property price
closing_fees = 2000 #in dollar cost
initial_disbursement = (((legal_costs + buying_tax) * property_price) + closing_fees + down_payment*property_price)
opportunity_cost = initial_disbursement * i
print(f"The initial disbursement from the own investment is {initial_disbursement:4.2f} USD")
print(f"And this will make to stop receiving interests of {opportunity_cost:4.2f} USD monthly as opportunity cost")


# In[43]:


#Owner monthly disbursement if property is bought, inluding financial and opportunity costs
condo_fees = 1055
property_tax = 300
maintenance_fee = 50

tot_monthly_outflow = condo_fees + property_tax + maintenance_fee + fnct_pmt(loan, i, n) + opportunity_cost
print(f"Total monthly disbursement during the life of the credit is {tot_monthly_outflow:4.2f}")

monthly_rent = 3000

#incremental monthly disbursement due to the acquisition of the property:
incremental_payment = tot_monthly_outflow - monthly_rent
print(f"The investor should make an incremental disbursement of {incremental_payment:4.2f} USD monthly, in order to be the owner of the property")


# ### Let see if the incremental disbursement is worth compared to the selling price of the property in year 2, 5 or 10
# 
# Scenarios:
#     A. The condo price remains unchanged
#     B. The condo price drops 10% over the next two years, then increases back to it's purchase price by the end of 5 years
#     C. The condo price increases annually by the annual rate of inflation of 2% over the next 10 years
#     D. The condo price increases annually by an annual rate of 5% over the next 10 years.

# In[ ]:




