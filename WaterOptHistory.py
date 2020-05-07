#!/usr/bin/env python
'''
    File name: Model.py
    Date created: 05/04/2018
    Date last modified: 10/04/2018
    Python Version: 3.6.5
'''
__author__ = "Yaswanth"
__copyright__ = "Copyright 2018, The BITS Project"


import pandas as pd
import string
from datetime import timedelta, datetime
from random import randint
import random
import xlrd
import sys

startDate = datetime(2017, 1, 1, 00, 00, 00)
now = datetime.now()
#mlist = [
#'12ABC45613AS34','12ABC45613AS35','12ABC45613AS36','12ABC45613AS37','12ABC45613AS38','12ABC45613AS39','12ABC45613AS40','12ABC45613AS41','12ABC45613AS42',#'12ABC45613AS43','12ABC45613AS44','12ABC45613AS45','12ABC45613AS46','12ABC45613AS47','12ABC45613AS48']
df = pd.DataFrame(columns=['Date','MeterNo','StrtTime','EndTime','Capacity','Entity','Consumption'])
df1 = pd.DataFrame(columns=['Date','MeterNo','StrtTime','EndTime','Capacity','Entity','Consumption'])
while(startDate < now):    
    print(startDate)
    mcl = list()
    mlist = ['12ABC45613AS34','12ABC45613AS35','12ABC45613AS36','12ABC45613AS37','12ABC45613AS38','12ABC45613AS39','12ABC45613AS40','12ABC45613AS41','12ABC45613AS42','12ABC45613AS43','12ABC45613AS44','12ABC45613AS45','12ABC45613AS46','12ABC45613AS47','12ABC45613AS48']
    b = randint(0,len(mlist))
    print(b)
    for i in range(0,b):
        mc = random.choice(mlist)
        mcl.append(mc)
        mlist.remove(mc)
        print(mc)
    if df.empty:
        df = pd.DataFrame({'MeterNo':mcl})
        df['Date'] = startDate
    else:
        df1 = pd.DataFrame({'MeterNo':mcl})
        df1['Date'] = startDate
        df = pd.concat([df,df1])
    startDate += timedelta(hours=1)
#df.to_excel('E:/MTech_Proj/watermeter.xlsx', index = False)
df1 = pd.read_excel('E:/MTech_Proj/Meter_Entity_Capa.xlsx')
dfT = pd.merge(df,df1,how = 'left', left_on = 'Meter_no', right_on = 'MeterNo')
del dfT['Meter_no']
dfT['Usage'] = dfT.apply(lambda x:randint(0,dfT['Capacity']), axis = 1)