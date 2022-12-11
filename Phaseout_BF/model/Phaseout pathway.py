import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")
BF_ALL = pd.read_csv(r'Input/input.csv',sep=',')
DRate=0.03
Lifetime=30
phaseoutscale = pd.read_csv(r'Input/phaseoutscale.csv',sep=',')
phaseoutscale=phaseoutscale.set_index('Year')
Phaseout_requirement=phaseoutscale*BF_ALL['Capacity'].sum()/1064767
print(Phaseout_requirement)

def Ginical (table_Gini):
    table_Gini=table_Gini.sort_values(by=['ratio'])
    range(0,table_Gini.shape[0]+1)
    table_Gini['count']=range(1,table_Gini.shape[0]+1)
    table_Gini['valuex']=table_Gini['count']/(table_Gini.shape[0])
    table_Gini['ratio_agg']=np.cumsum(table_Gini['ratio'])
    table_Gini['valuey']=table_Gini['ratio_agg']/table_Gini['ratio_agg'].max()
    table_Gini['value']=(table_Gini['valuex']-table_Gini['valuey'])/table_Gini['valuex']
    return table_Gini['value'].mean()

#The_baseline_scenario
for year in range(2021,2031):
    if year==2021:
        BFbaseline_list=BF_ALL
        basetable = pd.DataFrame({"year": "", "Carbon_effect_base": "", "Water_effect_base": "", "Health_effect_base": ""},index=["0"])
    else:
        BFbaseline_list=BFbaseline_list
    #Sort BF according to its cost
    BFbaseline_list['currentage']=year-BFbaseline_list['Start_yr']
    BFbaseline_list = BFbaseline_list[BFbaseline_list['currentage'] <30]
    #Calculate the economic loss and environmental effect
    BF_base_calculate=BFbaseline_list
    BF_base_calculate['health_effect']=BF_base_calculate['HEALTHpt']*BF_base_calculate['Capacity']*1000
    BF_base_calculate['water_effect']=BF_base_calculate['WATERRISKpt']*BF_base_calculate['Capacity']*1000
    BF_base_calculate['carbon_effect']=BF_base_calculate['CO2pt']*BF_base_calculate['Capacity']*1000
    Heal=BF_base_calculate['health_effect'].sum()
    Water=BF_base_calculate['water_effect'].sum()
    Carbon=BF_base_calculate['carbon_effect'].sum()
    baselinecalculate=pd.DataFrame({"year":year,"Carbon_effect_base":Carbon,"Water_effect_base":Water,"Health_effect_base":Heal},index=["0"])
    basetable=basetable.append(baselinecalculate,ignore_index=True)
basetable["Health_effect_base"]=pd.to_numeric(basetable["Health_effect_base"],errors='coerce').fillna(0)
basetable["Water_effect_base"]=pd.to_numeric(basetable["Water_effect_base"],errors='coerce').fillna(0)
basetable["Carbon_effect_base"]=pd.to_numeric(basetable["Carbon_effect_base"],errors='coerce').fillna(0)
print(basetable)


summarytable = pd.DataFrame()
summary2table = pd.DataFrame()
Province_total=BF_ALL.pivot_table(index=['Province'],values=['Capacity'],aggfunc='sum')

#The phaseout scenario with environmental adjust paramter
for adjust_factor in [0,0.2,0.5,1,2,5]:
    for weight in range(0,1000):
        print(str(adjust_factor)+" factor"+str(weight)+"_start")
        Ginicalculator = pd.DataFrame()
        a = random()
        b = random()
        c = random()
        ratio = a + b + c
        a = a / ratio
        b = b / ratio
        c = c / ratio
        Economic2=0
        Carbon2=0
        Water2=0
        Health2=0
        for Decision_year in range(2021,2031):
            if Decision_year==2021:
                BF_list=BF_ALL
            else:
                BF_list=BF_list
            #Sort BF according to its cost
            BF_list['profit_loss'] = npf.pv(DRate, 30 - (Decision_year - BF_list['Start_yr']), -((850 - BF_list['Pro_cost']) * 0.8))
            BF_list['stranded_assets'] = BF_list['INVESTpt'] / Lifetime * (Lifetime - (Decision_year - BF_list['Start_yr']))
            BF_list['cost' + str(Decision_year)] = BF_list['profit_loss'] + BF_list['stranded_assets']
            BF_list['Environmental_index']= a*BF_list['CO2_index']+b*BF_list['Water_index']+c*BF_list['Health_index']
            BF_list['cost_adj_'+str(Decision_year)]=BF_list['cost' + str(Decision_year)]/pow(BF_list['Environmental_index'],adjust_factor)
            BF_sort=BF_list.sort_values(by=['cost_adj_'+str(Decision_year)])
            BF_sort['cumulativecapacity']=np.cumsum(BF_sort['Capacity'])
            BF_phaseout=BF_sort[BF_sort['cumulativecapacity'] <= Phaseout_requirement.loc[Decision_year,'phaseout']]
            BF_phaseout['economic_losses'] = BF_phaseout['cost' + str(Decision_year)]*BF_phaseout['Capacity']*1000
            Ginicalculator=Ginicalculator.append(BF_phaseout,ignore_index=True)
            #Calculate the economic loss and environmental effect
            Econ=BF_phaseout['economic_losses'].sum()+BF_phaseout['cost'+str(Decision_year)].max()*1000*(Phaseout_requirement.loc[Decision_year,'phaseout']-BF_phaseout['Capacity'].sum())
            BF_list=BF_sort[BF_sort['cumulativecapacity'] > Phaseout_requirement.loc[Decision_year,'phaseout']]
            BF_calculate=BF_list
            BF_calculate['health_effect']=BF_calculate['HEALTHpt']*BF_calculate['Capacity']*1000
            BF_calculate['water_effect']=BF_calculate['WATERRISKpt']*BF_calculate['Capacity']*1000
            BF_calculate['carbon_effect']=BF_calculate['CO2pt']*BF_calculate['Capacity']*1000
            Heal=basetable.loc[Decision_year-2020,"Health_effect_base"] - BF_calculate['health_effect'].sum()
            Water=basetable.loc[Decision_year-2020,"Water_effect_base"] - BF_calculate['water_effect'].sum()
            Carbon=basetable.loc[Decision_year-2020,"Carbon_effect_base"] - BF_calculate['carbon_effect'].sum()
            pdcalculate=pd.DataFrame({"year":Decision_year,"weight":weight,"factor":adjust_factor,"economic_losses":Econ,"Carbon_effect":Carbon,"Water_effect":Water,"Health_effect":Heal},index=["0"])
            summarytable=summarytable.append(pdcalculate,ignore_index=True)
            Economic2=Economic2+Econ*pow(1-DRate,Decision_year-2021)
            Carbon2=Carbon2+Carbon*pow(1-DRate,Decision_year-2021)
            Water2=Water2+Water*pow(1-DRate,Decision_year-2021)
            Health2=Health2+Heal*pow(1-DRate,Decision_year-2021)
        #Gini coefficient calculation
        Province1 = Ginicalculator.pivot_table(index=['Province'],values=['Capacity'],aggfunc='sum')
        Province1.rename(columns={'Capacity':'Phaseout'},inplace=True)
        Ginitable=pd.merge(Province_total,Province1,how='left',on='Province')
        Ginitable=Ginitable.fillna(0)
        Ginitable['ratio']=Ginitable['Phaseout']/Ginitable['Capacity']
        Gini=Ginical(Ginitable)
        summary2table=summary2table.append(pd.DataFrame({'weight':weight,'factor':adjust_factor,'economic_losses':Economic2,'Carbon':Carbon2,'Water':Water2,'Health':Health2,'Gini':Gini},index=[0]),ignore_index=True)

summarytable.to_csv('output/allscenariosoutput.csv')
summary2table['economic_loss_2']=summary2table['economic_losses']/summary2table.loc[0,'economic_losses']
summary2table['Carbon_2']=summary2table['Carbon']/summary2table.loc[0,'Carbon']
summary2table['Water_2']=summary2table['Water']/summary2table.loc[0,'Water']
summary2table['Health_2']=summary2table['Health']/summary2table.loc[0,'Health']
summary2table['Carbon_3']=summary2table['Carbon_2']/summary2table['economic_loss_2']
summary2table['Water_3']=summary2table['Water_2']/summary2table['economic_loss_2']
summary2table['Health_3']=summary2table['Health_2']/summary2table['economic_loss_2']
summary2table.to_csv('output/allscenariooutput2.csv')

def EEtype(EE):
    if EE>1:
        return 1
    else:
        return 0


summary2table['Carbon_4']=summary2table.apply(lambda x: EEtype(x['Carbon_3']),axis=1)
summary2table['Water_4']=summary2table.apply(lambda x: EEtype(x['Water_3']),axis=1)
summary2table['Health_4']=summary2table.apply(lambda x: EEtype(x['Health_3']),axis=1)
summary2table['EE_type']=summary2table['Carbon_4']+summary2table['Water_4']+summary2table['Health_4']
summary2table.to_csv('output/allscenariooutput2.csv')