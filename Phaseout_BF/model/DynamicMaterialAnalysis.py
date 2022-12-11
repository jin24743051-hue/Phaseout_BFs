import pandas as pd
import numpy as np
import statsmodels.api as sm
import math


def retireratio (type,life):
    if type == 'construction':
        a=30
        b=15
    if type == 'machinery':
        a=20
        b=10
    if type == 'transportation':
        a=15
        b=7.5
    if type == 'others':
        a=15
        b=7.5
    if life == 0:
        ratio=0
    else:
        ratio=1/(b*pow(2*math.pi,0.5))*np.exp(-pow(life-a,2)/(2*b*b))
    return ratio

def saturate (type):
    if type == 'construction':
        value=6.8
    if type == 'machinery':
        value=2
    if type == 'transportation':
        value=1
    if type == 'others':
        value=1.8
    return value

def regress (data1,data2):
    x=np.array(data1)
    X=sm.add_constant(x)
    y=np.array(data2)
    regress= sm.OLS(y,X).fit()
    return regress.params

def consumption (type):
    if type == 'construction':
        value=0.53
    if type == 'machinery':
        value=0.19
    if type == 'transportation':
        value=0.08
    if type == 'others':
        value=0.2
    return value

data=pd.read_csv(r'C:\Users\HERO\Desktop\Phaseoutmodel\DMA\Input.csv',sep=',')
data_year=data.set_index('Year')
data_year['pc_GDP']=data_year['GDP']/data_year['Population']
#Consumption calculation
data_year['Consumption']=data_year['Output']-data_year['Export']+data_year['Import'] - data_year['Indirect_net_export']
for k in ('construction', 'machinery', 'transportation', 'others'):
    data_year['Consumption_'+str(k)]=data_year['Consumption']*consumption(k)

#Scrap calculation
for i in range(1983,2021):
    for k in ('construction', 'machinery', 'transportation', 'others'):
        scrap=0
        for j in range(1983,i+1):
            scrap=scrap+data_year.loc[j, 'Consumption_' + str(k)]*retireratio(k,i-j)
        data_year.loc[i,'scrap_'+str(k)]=scrap

#Stock calculation
for i in range(1983,2021):
    for k in ('construction', 'machinery', 'transportation', 'others'):
        stock=0
        for j in range(1983, i + 1):
            stock=stock+data_year.loc[j,'Consumption_'+str(k)]-data_year.loc[j,'scrap_'+str(k)]
        data_year.loc[i, 'stock_' + str(k)] = stock
for k in ('construction', 'machinery', 'transportation', 'others'):
    data_year['pc_stock_'+str(k)]=data_year['stock_'+str(k)]/data_year['Population']

#regressvariable
for k in ('construction', 'machinery', 'transportation', 'others'):
    data_year['reg_'+str(k)]=np.log(saturate(k)/data_year['pc_stock_'+str(k)]-1)

data_reg=data_year.loc[:,'reg_construction':'reg_others']
data_reg['pc_GDP']=data_year['pc_GDP']
data_reg.to_csv('DMA/reg.csv')

#future prediction
#SSP scenario input: population and GDP
SSPdata=pd.read_csv(r'C:\Users\HERO\Desktop\Phaseoutmodel\DMA\SSP_input.csv',sep=',')
SSPdata_year=SSPdata.set_index('Year')
prediction=pd.concat([data_year,SSPdata_year])
prediction['pc_GDP']=prediction['GDP']/prediction['Population']
#future pc_stock calculation
for i in range(2021,2051):
    for k in ('construction', 'machinery', 'transportation', 'others'):
        prediction.loc[i,'reg_'+str(k)]=regress(data_year.loc[2000:2020,'pc_GDP'],data_year.loc[2000:2020,'reg_'+str(k)])[0]+\
                                        prediction.loc[i,'pc_GDP']*regress(data_year.loc[2000:2020,'pc_GDP'],data_year.loc[2000:2020,'reg_'+str(k)])[1]
        prediction.loc[i,'pc_stock_'+str(k)]=saturate(k)/(np.exp(prediction.loc[i,'reg_'+str(k)])+1)
for k in ('construction', 'machinery', 'transportation', 'others'):
    prediction['stock_'+str(k)]=prediction['pc_stock_'+str(k)]*prediction['Population']

#future output and scrap calculation
for i in range(2021,2051):
    for k in ('construction', 'machinery', 'transportation', 'others'):
        scrap=0
        for j in range(1983,i):
            scrap=scrap+prediction.loc[j, 'Consumption_' + str(k)]*retireratio(k,i-j)
        prediction.loc[i, 'scrap_' + str(k)] = scrap
        prediction.loc[i,'Consumption_'+str(k)]=prediction.loc[i, 'scrap_' + str(k)]+prediction.loc[i,'stock_'+str(k)]-\
                                                    prediction.loc[i-1,'stock_'+str(k)]
    prediction.loc[i,'Export']=prediction.loc[2010:2020,'Export'].mean()
    prediction.loc[i,'Import']=prediction.loc[2010:2020,'Import'].mean()
    prediction.loc[i,'Indirect_net_export'] = prediction.loc[2010:2020, 'Indirect_net_export'].mean()
prediction['Consumption']=prediction['Consumption_construction']+prediction['Consumption_machinery']+\
                          prediction['Consumption_transportation']+prediction['Consumption_others']
prediction['Output']=prediction['Consumption']+prediction['Export']-prediction['Import']+prediction['Indirect_net_export']
prediction['totalscrap']=prediction['scrap_construction']+prediction['scrap_machinery']+\
                         prediction['scrap_transportation']+prediction['scrap_others']

Ratio=9795.8/prediction.loc[2020,'totalscrap']
prediction['EAF_ratio']=prediction['totalscrap']*Ratio/prediction['Output']

#results analysis
outputfile=pd.DataFrame()
for m in ('Output','EAF_ratio','stock_construction','stock_machinery','stock_transportation','stock_others'):
    outputfile[str(m)]=prediction[str(m)]
outputfile['BF']=outputfile['Output']*(1-outputfile['EAF_ratio'])
outputfile['EAF']=outputfile['Output']-outputfile['BF']
outputfile.to_csv('DMA/output.csv')
phaseoutscale=pd.DataFrame()
phaseoutscale['Year']=range(2021,2031)
phaseoutscale=phaseoutscale.set_index('Year')
for i in range(2021,2031):
    phaseoutscale.loc[i,'phaseout']=(outputfile.loc[i-1,'BF']-outputfile.loc[i,'BF'])*10
phaseoutscale.to_csv('input/phaseoutscale.csv')
print(outputfile.loc[2050,'BF'])
print(outputfile)


