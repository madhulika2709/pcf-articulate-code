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
from random import randint
import pandas as pd
import string
from datetime import timedelta, datetime
import random
import xlrd
import sys
import numpy as np
df = pd.read_excel('E:/MTech_Proj/Meter_Entity_Capa.xlsx')
df1 = pd.read_excel('E:/MTech_Proj/watermeterTtest.xlsx')

dfn = pd.DataFrame(columns=['Date','MeterNo','StrtTime','EndTime'])
#df1 = pd.DataFrame(columns=['Date','MeterNo','StrtTime','EndTime','Capacity','Entity','Consumption'])

startDate = (max(df1['Date']))
startDate += timedelta(hours=1)
now = datetime.now()
#df['Capacity'] = pd.to_numeric(df['Capacity'], errors='coerce').fillna(0).astype(np.int64)
while(startDate < now):    
    print(startDate)
    dfn = pd.DataFrame(columns=['Date','MeterNo'])
    mcl = list()
    mlist = ['12ABC45613AS34','12ABC45613AS35','12ABC45613AS36','12ABC45613AS37','12ABC45613AS38','12ABC45613AS39','12ABC45613AS40','12ABC45613AS41','12ABC45613AS42','12ABC45613AS43','12ABC45613AS44','12ABC45613AS45','12ABC45613AS46','12ABC45613AS47','12ABC45613AS48']
    b = randint(0,len(mlist))
    print(b)
    for i in range(0,b):
        mc = random.choice(mlist)
        mcl.append(mc)
        mlist.remove(mc)
        print(mc)
    dfn['MeterNo'] = mcl
    dfn['Date'] = startDate
    dfn = pd.merge(dfn,df,how = 'left', left_on = 'MeterNo', right_on = 'Meter_no')
    #dfn.to_excel('E:/MTech_Proj/Testexcel.xlsx', index= False)
    del dfn['MeterNo']    
    dfn['Usage'] = dfn.apply(lambda x:randint(0,x['Capacity']), axis = 1)
    dfn['srtTime'] = dfn.apply(lambda x:randint(0,59), axis = 1)
    dfn['srtTime'] = dfn.apply(lambda x:43 if x['srtTime']== 59 else x['srtTime'], axis = 1)
    dfn['endTime'] = dfn.apply(lambda x:randint(x['srtTime'] + 1, 59), axis = 1)    
    df1 = pd.concat([df1,dfn])
    del dfn
    startDate += timedelta(hours=1)

#dfT = pd.merge(df1,df,how = 'left', left_on = 'MeterNo', right_on = 'Meter_no')
#print(dfT.head(5))
df1.to_excel('E:/MTech_Proj/watermeterTtest.xlsx', index= False)
#del dfT['Meter_no']
#dfT['Usage'] = dfT.apply(lambda x:randint(0,x['Capacity']), axis = 1)
#dfT['srtTime'] = dfT.apply(lambda x:randint(0,59), axis = 1)
#dfT['srtTime'] = dfT.apply(lambda x:43 if x['srtTime']== 59 else x['srtTime'], axis = 1)
#dfT['endTime'] = dfT.apply(lambda x:randint(x['srtTime'] + 1, 59), axis = 1)
#dfT.to_excel('E:/MTech_Proj/watermeterTN.xlsx', index= False)