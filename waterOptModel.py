#!/usr/bin/env python
'''
    File name: Model.py
    Date created: 05/04/2018
    Date last modified: 10/04/2018
    Python Version: 3.6.5
'''
__author__ = "Yaswanth"
__copyright__ = "Copyright 2018, The BITS Project"

import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import timedelta, datetime

df = pd.read_excel('E:/MTech_Proj/watermeterTtest.xlsx')

#The Average consumption Analysis code

now = datetime.now()
df_lastH = df[df['Date']==now.replace(minute=00, second = 00, microsecond = 00)-timedelta(hours=1)]
df_lastHApt = df_lastH[df_lastH['Segment']=='Apartment']
aptM = df_lastHApt['Usage'].mean()
df_lastHApt['hi_users'] = df_lastHApt.apply(lambda x: 'yes' if x['Usage'] > aptM else 'No',axis = 1)
print(df_lastHApt)


#### Arima prediction model  ####
df['ActualDate'] = df.apply(lambda x: datetime.date(x['Date']),axis = 1)
df_daily = df.groupby(['ActualDate', 'Meter_no','Entity','Segment'])['Usage'].mean()
#df_daily.to_excel('E:/MTech_Proj/waterAvg.xlsx')
df_daily = pd.DataFrame(df_daily)
df_daily_aptA = df_daily[df_daily['Entity'] == ' Apartment - A']

   ## model input
df_daily_aptAMI = df_daily_aptA[['ActualDate','Usage']]

df_cp = df_daily_aptAMI.copy()

df_cp.set_index(['ActualDate'], inplace = True)
df_cp.plot(figsize=(15, 6))
plt.show()
# Define p,d,q values to take certain values i.e. 0 to 2
p = d = q = range(0,2)
# Generate different combinations of p,d,q
pdq = list(itertools.product(p,d,q))
# Generate all different combinations of seasonal p, d and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
# Validation through AIC
warnings.filterwarnings("ignore") # specify to ignore warning messages
for param in pdq:    
    for param_seasonal in seasonal_pdq:        
        try:
            mod = sm.tsa.statespace.SARIMAX(df_cp,order=param,seasonal_order=param_seasonal,enforce_stationarity=False,enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            #print("error thrown")
            continue

print(df_cp.head(n=5))
mod = sm.tsa.statespace.SARIMAX(df_cp,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
#ARIMA(0, 0, 1)x(4, 0, 0, 12)12 - AIC:56.34977812415613
# (0,3,0) X (3,1,0)
#(1,2,2) X (3,1,0)
#(2,3,0) X (2,2,0)
#(2,3,0) X (3,1,0)
#(3,3,0) X (1,3,0)
#(3,3,2) X (2,2,0)
results = mod.fit()
#print(results.summary().tables[1])
results.plot_diagnostics(figsize=(15, 6))
plt.show()
pred = results.get_prediction(start=pd.to_datetime('2019-01-01'), dynamic=False)
pred_ci = pred.conf_int()
print(pred)
print(pred_ci[pred_ci.columns[1]].to_string(index = False))
print(pred_ci.head(n=5))
ax = df_cp['2014-7-01':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)
ax.fill_between(pred_ci.index,pred_ci.iloc[:, 0],pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Crude Petroleum')
plt.legend()
plt.show()
df_cp_forecasted = pred.predicted_mean
df_cp_forecasted1 = pd.DataFrame(df_cp_forecasted)
df_cp_truth = df_cp['2007-01-01':]
#print(df_cp_forecasted1.head(n=5))
#print(df_cp_truth.head(n=5))
#print(df_cp_forecasted1[0] -df_cp_truth['CrudePetroleum'] )
# Compute the mean square error
mse = (np.square(df_cp_forecasted1[0] -df_cp_truth['CrudePetroleum'])).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print(df_cp_forecasted1[df_cp_forecasted1.columns[0]].to_string(index = False))

pred_dynamic = results.get_prediction(start = pd.to_datetime('2019-01-01'), dynamic = True, full_results = True)
pred_dynamic_ci = pred_dynamic.conf_int()

ax = df_cp['2017':].plot(label='observed', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)
ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)
ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2010-01-01'), df_cp.index[-1],
                 alpha=.1, zorder=-1)
ax.set_xlabel('Date')
ax.set_ylabel('Crude Petroleum')
plt.legend()
plt.show()