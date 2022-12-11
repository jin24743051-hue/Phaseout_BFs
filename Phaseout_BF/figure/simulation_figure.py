import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image


sns.set_theme()
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

def process(dfinput,variable,type):
    dfoutput=pd.DataFrame()
    for s in range(0,len(variable)):
        dfinput[str(type)]=variable[s]
        dfinput[str(type)+'_value']=dfinput[str(variable[s])]
        dfoutput=pd.concat([dfoutput,dfinput])
    return dfoutput

# Figure 8: the future trend
def stress(x):
    if x==0:
        y="factor=0"
    else:
        y="Others"
    return y
sns.set_theme(style="ticks")
df=pd.read_csv('output/allscenariosoutput.csv')
df['size']=df.apply(lambda x:stress(x['factor']),axis=1)
df['Health_effect']=df['Health_effect']/1000
df=df.sort_values(by=['factor'],ascending=False)

# Figure 8-1
sns.lineplot(data=df, x='year', y='economic_losses', hue='factor', errorbar='sd',size='size',legend=False,\
             hue_order=(5.0,2.0,1.0,0.5,0.2,0),size_order=('factor=0','Others'),palette=sns.color_palette("bright",n_colors=6))
plt.ylabel('EC($)',fontdict={'family':'Times New Roman','size':16})
plt.xlabel(' ',fontdict={'size':16})
plt.savefig('figure/futuretrend-1.png',dpi=500)
transPNG('figure/futuretrend-1.png')

plt.cla()
# Figure 8-2
sns.lineplot(data=df, x='year', y='Carbon_effect', hue='factor', errorbar='sd', size='size', \
             hue_order=(5.0, 2.0, 1.0, 0.5, 0.2, 0.0),size_order=('factor=0','Others',),legend=False,palette=sns.color_palette("bright",n_colors=6))
plt.ylabel('EB_carbon(ton)',fontdict={'family':'Times New Roman','size':16})
plt.xlabel(' ',fontdict={'size':16})
plt.savefig('figure/futuretrend-2.png',dpi=500)
transPNG('figure/futuretrend-2.png')
sns.lineplot()
plt.cla()
# Figure 8-3
sns.lineplot(data=df, x='year', y='Water_effect', hue='factor', errorbar='sd', size='size', \
             hue_order=(5.0, 2.0, 1.0, 0.5, 0.2, 0.0),size_order=('factor=0','Others',),legend=False,palette=sns.color_palette("bright",n_colors=6))
plt.ylabel('EB_water',fontdict={'family':'Times New Roman','size':16})
plt.xlabel('Year',fontdict={'size':16})
plt.savefig('figure/futuretrend-3.png',dpi=500)
transPNG('figure/futuretrend-3.png')
sns.lineplot()
plt.cla()
# Figure 8-4
sns.lineplot(data=df, x='year', y='Health_effect', hue='factor', errorbar='sd', size='size', \
             hue_order=(5.0, 2.0, 1.0, 0.5, 0.2, 0.0),size_order=('factor=0','Others',),legend=False, palette=sns.color_palette("bright",n_colors=6))
plt.ylabel('EB_health(1000 DALY)',fontdict={'family':'Times New Roman','size':16})
plt.xlabel('Year',fontdict={'size':16})
plt.savefig('figure/futuretrend-4.png',dpi=500)
transPNG('figure/futuretrend-4.png')

# Figure 9: the distribution of carbon-water-health index
df= pd.read_csv('Input/input.csv')
df=df.rename(columns={'CO2_index':'CO$_2$_index'})
df2=process(df,['CO$_2$_index','Health_index','Water_index'],'environmental_effect')
sns.catplot(data=df2, kind="violin", x='environmental_effect', y="environmental_effect_value", split=True)
plt.xlabel('')
plt.ylabel('value')
plt.savefig('figure/index_distribution.png')
transPNG('figure/index_distribution.png')

# Figure 10： the TEB and TEC
# Figure 10-1 TEC
df=pd.read_csv('Output/allscenariooutput2.csv')
df=df.loc[:,('factor','economic_losses','Carbon','Water','Health')]
df.columns=['adjust_factor','TEC','TEB_carbon','TEB_water','TEB_health']
df['TEB_health']=df['TEB_health']/1000
sns.catplot(
    data=df, x="adjust_factor", y="TEC",
    kind="box", dodge=False,
)
plt.xlabel('adjust_factor')
plt.ylabel('TEC($)')
plt.savefig('figure/TEC.png')
transPNG('figure/TEC.png')
plt.cla()
# Figure 10-2 TEB_carbon
sns.catplot(
    data=df, x="adjust_factor", y="TEB_carbon",
    kind="box", dodge=False,
)
plt.xlabel('adjust_factor')
plt.ylabel('TEB_carbon(ton)')
plt.savefig('figure/TEB_carbon.png')
transPNG('figure/TEB_carbon.png')
plt.cla()
# Figure 10-3 TEB_water
sns.catplot(
    data=df, x="adjust_factor", y="TEB_water",
    kind="box", dodge=False,
)
plt.xlabel('adjust_factor')
plt.ylabel('TEB_water')
plt.savefig('figure/TEB_water.png')
transPNG('figure/TEB_water.png')
plt.cla()
# Figure 10-4 TEB_health
sns.catplot(
    data=df, x="adjust_factor", y="TEB_health",
    kind="box", dodge=False,
)
plt.xlabel('adjust_factor')
plt.ylabel('TEB_health(1000 DALYs)')
plt.savefig('figure/TEB_health.png')
transPNG('figure/TEB_health.png')
plt.cla()


# Figure 11: the REB and REC
df=pd.read_csv('Output/allscenariooutput2.csv')
df=df.loc[:,('factor','economic_loss_2','Carbon_2','Water_2','Health_2')]
df=df[df['factor']>0]
df.columns=['adjust_factor','REC','REB_carbon','REB_water','REB_health']
df=df.sort_values(by=['adjust_factor'],ascending=False)
df['adjust_factor'] = df['adjust_factor'].astype(str)
sns.pairplot(data=df, hue="adjust_factor", palette=sns.color_palette("dark",n_colors=5))
plt.savefig('figure/economic_carbon_water_health.png')
transPNG('figure/economic_carbon_water_health.png')


# Figure 12: Box plot of EE
df=pd.read_csv('Output/allscenariooutput2.csv')
df=df.loc[:,('factor','Carbon_3','Water_3','Health_3')]
df['adjust_factor']=df['factor']
df['EE_carbon']=df['Carbon_3']
df['EE_water']=df['Water_3']
df['EE_health']=df['Health_3']
df=process(df,('EE_carbon','EE_water','EE_health'),'Type')
sns.catplot(data=df, x="Type", y="Type_value", hue="adjust_factor", kind="box",legend_out=False)
plt.xlabel('')
plt.ylabel('Value')
plt.savefig('figure/relative_costbenefit.png',dpi=500)
transPNG('figure/relative_costbenefit.png')

# Figure 13: the Gini coefficient
df=pd.read_csv('Output/allscenariooutput2.csv')
df=df.loc[:,('factor','Gini')]
sns.catplot(
    data=df, x="factor", y="Gini",
    kind="box", dodge=False,
)
plt.xlabel('adjust_factor')
plt.ylabel('GCRR')
plt.savefig('figure/Gini.png',dpi=500)
transPNG('figure/Gini.png')

# Figure 13:  EE_type
df=pd.read_csv('Output/allscenariooutput2.csv')
df=df.loc[:,('factor','EE_type')]
df=df[df['factor']>0]
df['factor'] = df['factor'].astype(str)
ax=sns.histplot(df, x="factor", hue="EE_type", multiple="stack",weights=10,shrink=0.5)
plt.xlabel('adjust_factor')
plt.savefig('figure/EEtype.png')
transPNG('figure/EEtype.png')


# Figure 14-1: the efficiency vs equality
df=pd.read_csv('Output/optimization.csv')
df['Environmental_efficiency']=df['Carbon_3']+df['Water_3']+df['Health_3']
sns.jointplot(data=df, x="Gini", y="Environmental_efficiency", hue="EE_type",hue_order=(3,2,1,0),palette=sns.color_palette("dark",n_colors=4))
plt.xlabel('GCRR')
plt.xticks()
plt.ylabel('TEE')
plt.savefig('figure/EEtradeoff1.png')
transPNG('figure/EEtradeoff1.png')

# Figure 14-2: the efficiency vs equality
df=pd.read_csv('Output/optimization.csv')
df['Environmental_efficiency']=df['Carbon_3']+df['Water_3']+df['Health_3']
df=df[df['EE_type']==3]
df['adjust_factor']=df['factor']
sns.jointplot(data=df, x="Gini", y="Environmental_efficiency", hue='adjust_factor',legend='full')
plt.xlabel('GCRR')
plt.ylabel('TEE')
plt.legend(loc='best')
plt.savefig('figure/EEtradeoff2.png')
transPNG('figure/EEtradeoff2.png')
