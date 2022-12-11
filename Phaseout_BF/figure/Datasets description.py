import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

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


# Figure 1: the age structure of BFs
df= pd.read_csv('Input/input.csv')
df['BF_type']=df.apply(lambda x: classtype(x['Capacity']),axis=1)
df['Capacity']=df['Capacity']/1000
ax=sns.histplot(df, x="Start_yr", hue="BF_type", weights='Capacity',hue_order=('<0.5 MTPY','0.5~1 MTPY','1~2 MTPY','>2 MTPY'), multiple="stack", kde=True)
plt.xlabel('Start_year',fontdict={'family':'Times New Roman','size':16})
plt.ylabel('Total Capacity (MTPY)',fontdict={'family':'Times New Roman','size':16})
plt.xticks(fontproperties='Times New Roman', size=15)
plt.yticks(fontproperties='Times New Roman', size=15)
plt.tight_layout()
plt.savefig('figure/BF_type.png',dpi=500)
transPNG('figure/BF_type.png')


# Figure 2: the distribution of variablees
df= pd.read_csv('Input/input.csv')
df=df.loc[:,('INVESTpt','Pro_cost','CO2pt','SO2pt','PMpt','NOXpt','WATERpt','HEALTHpt','WATERRISKpt')]
sns.displot(data=df, x="INVESTpt", kde=True)
plt.xlabel('Per-unit fixed cost($/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/Fixedcost.png',dpi=500)
transPNG('figure/Fixedcost.png')

sns.displot(data=df, x="Pro_cost", kde=True,bins=20)
plt.xlabel('Per-unit production cost($/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/Pro_cost.png', dpi=500)
transPNG('figure/Pro_cost.png')

sns.displot(data=df, x="CO2pt", kde=True,bins=20)
plt.xlabel('Per-unit CO2 emission(t/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/CO2.png',dpi=500)
transPNG('figure/CO2.png')

sns.displot(data=df, x="SO2pt", kde=True, bins=20)
plt.xlabel('Per-unit SO2 emission(kg/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks( size=15)
plt.yticks(size=15)
plt.savefig('figure/SO2.png',dpi=500)
transPNG('figure/SO2.png')

sns.displot(data=df, x="PMpt", kde=True, bins=20)
plt.xlabel('Per-unit PM2.5 emission(kg/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/PM25.png',dpi=500)
transPNG('figure/PM25.png')

sns.displot(data=df, x="NOXpt", kde=True, bins=20)
plt.xlabel('Per-unit NOx emission(kg/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/NOX.png',dpi=500)
transPNG('figure/NOX.png')

sns.displot(data=df, x="WATERpt", kde=True, bins=20)
plt.xlabel('Per-unit water consumption(m$^3$/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/Water.png',dpi=500)
transPNG('figure/Water.png')

df['HEALTHpt']=df['HEALTHpt']*100000
sns.displot(data=df, x="HEALTHpt", kde=True,bins=20)
plt.xlabel('Per-unit health burden(10$^-$$^5$ DALY/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks(size=15)
plt.yticks(size=15)
plt.savefig('figure/Health.png',dpi=500)
transPNG('figure/Health.png')

sns.displot(data=df, x="WATERRISKpt", kde=True,bins=20)
plt.xlabel('Per-unit water stress(/t)',fontdict={'size':16})
plt.ylabel('Count',fontdict={'size':16})
plt.xticks( size=15)
plt.yticks( size=15)
plt.savefig('figure/Stress.png',dpi=500)
transPNG('figure/Stress.png')

# Figure 3: the heatmap of varibales
df= pd.read_csv('Input/input.csv')
df=df.loc[:,('Age','Capacity','INVESTpt','Pro_cost','CO2pt','SO2pt','PMpt','NOXpt','WATERpt','HEALTHpt','WATERRISKpt')]
df=df.rename(columns={'Pro_cost':'PROCOSTpt'})
df=df.rename(columns={'WATERRISKpt':'WATERSTRESSpt'})
df_coor=df.corr()
sns.heatmap(df_coor, vmax=1, square=True,annot=True, cmap="Blues", fmt='.1g')
plt.tight_layout()
plt.savefig('figure/Heatmap.png')
transPNG('figure/Heatmap.png')


