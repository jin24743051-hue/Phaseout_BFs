import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import math
import statsmodels.api as sm



def process(dfinput,variable,type):
    dfoutput=pd.DataFrame()
    for s in range(0,len(variable)):
        dfinput[str(type)]=variable[s]
        dfinput[str(type)+'_value']=dfinput[str(variable[s])]
        dfoutput=pd.concat([dfoutput,dfinput])
    return dfoutput

def classtype(capacity):
    if capacity<500:
        BF_type='<0.5 MTPY'
    if (capacity>=500 and capacity<1000):
        BF_type='0.5~1 MTPY'
    if (capacity>=1000 and capacity<2000):
        BF_type='1~2 MTPY'
    if (capacity>=2000):
        BF_type='>2 MTPY'
    return BF_type

#convert png file with white background into transparent
def transPNG(ImageName):
    img=Image.open(ImageName)
    img=img.convert('RGBA')
    datas=img.getdata()
    newData=list()
    for item in datas:
        if item[0]==255 and item[1]==255 and item[2]==255:
            newData.append((0,0,0,0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(ImageName)

sns.set_theme()


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


# Figure 4: the BF prediction of DMA analysis
df=pd.DataFrame()
df['year']=range(1,80)
for j in ('construction','machinery','transportation','others'):
    for i in range (0,79):
        df.loc[i,str(j)]=retireratio(str(j),df.loc[i,'year'])

df=process(df, ('construction','machinery','transportation','others'), 'steel products')
sns.lineplot(
    data=df,
    x="year", y="steel products_value",
    hue="steel products"
)
plt.legend(loc='upper right')
plt.xlabel('Life time',fontdict={'family':'Times New Roman'})
plt.ylabel('Scrap probability',fontdict={'family':'Times New Roman'})
plt.savefig('figure/survival.png',dpi=500)
transPNG('figure/survival.png')

# Figure 5: the regress results
df = pd.read_csv('DMA/reg.csv')
df=df.loc[17:37,:]
df.columns=['Year','construction','machinery','transportation','others','pc_GDP']
df=process(df,('construction','machinery','transportation','others'),'steel products')
sns.lmplot(x="pc_GDP", y="steel products_value", hue='steel products', data=df, legend_out=False)
plt.xlabel('Per capita GDP (10000CNY/person)',fontdict={'family':'Times New Roman'})
plt.ylabel('Dependent variables',fontdict={'family':'Times New Roman'})
plt.savefig('figure/regress.png',dpi=500)
transPNG('figure/regress.png')

x = np.array(df['pc_GDP'])
X = sm.add_constant(x)
y = np.array(df['construction'])
regress = sm.OLS(y, X).fit()
print(regress.summary())
y = np.array(df['machinery'])
regress = sm.OLS(y, X).fit()
print(regress.summary())
y = np.array(df['transportation'])
regress = sm.OLS(y, X).fit()
print(regress.summary())
y = np.array(df['others'])
regress = sm.OLS(y, X).fit()
print(regress.summary())

# Figure 6:the future stock for four types
df=pd.read_csv('DMA/output.csv')
df=df[df['Year']>=2020]
df['stock_construction']=df['stock_construction']/100000
df['stock_machinery']=df['stock_machinery']/100000
df['stock_transportation']=df['stock_transportation']/100000
df['stock_others']=df['stock_others']/100000
x=df['Year'].tolist()
y1=df['stock_construction'].tolist()
y2=df['stock_machinery'].tolist()
y3=df['stock_transportation'].tolist()
y4=df['stock_others'].tolist()
plt.stackplot(x,y1,y2,y3,y4,labels=['construction','machinery','transportation','others'])
plt.xlabel('Year')
plt.ylabel('In-use steel stock (Gt)')
plt.legend(loc='lower right')
plt.savefig('figure/Futurestock.png')
transPNG('figure/Futurestock.png')

# Figure 7: the BF prediction of DMA analysis
df=pd.read_csv('DMA/output.csv')
df=df[df['Year']>=2020]
df['BF']=df['BF']/100
df['EAF']=df['EAF']/100
x=df['Year'].tolist()
y1=df['BF'].tolist()
y2=df['EAF'].tolist()
plt.stackplot(x,y1,y2,colors=['r','c'],labels=['BF process','EAF process'])
plt.xlabel('Year')
plt.ylabel('Crude steel production (MT)')
plt.legend(loc='upper right')
plt.savefig('figure/BFprediction.png')
transPNG('figure/BFprediction.png')



