import pandas as pd
import time
pd.options.mode.chained_assignment = None

def prepareFolders():
    import os
    if not os.path.exists('analysisData'):
        os.makedirs('analysisData')

def balanceFund(dfs,wallet):
    dfs = dfs.iloc[:-5]
    divident = wallet / 15
    dfs['Field5'] = dfs['Field5'].str.replace('$', '')
    dfs['Field5'] = dfs['Field5'].str.replace(',', '')
    dfs['Field5'] = dfs['Field5'].astype(float)
    dfs['holdings'] = divident / dfs['Field5']
    dfs['holdings'] = dfs['holdings'].replace(float('inf'), 1)
    return dfs

def calcHoldings(dfs):
    temps = pd.merge(temp, dfs, how='inner', on='Field3')
    temps['Field5_y'] = temps['Field5_y'].str.replace('$', '')
    temps['Field5_y'] = temps['Field5_y'].str.replace(',', '')
    temps['holdings'] = temps['holdings'].astype(float)
    temps['Field5_y'] = temps['Field5_y'].astype(float)
    temps['total_holdings_in_$'] = temps['holdings'] * temps['Field5_y']
    total_holdings = temps['total_holdings_in_$'].sum()
    temps = temps.rename(columns={'Field5_y': 'current_price'})
    temps = temps.rename(columns={'Field5_x': 'previous_price'})
    temps.to_csv('analysisData/'+startDate.replace('/', '-')+'.csv', index=False)
    return total_holdings


df = pd.read_csv("coinCapSim.csv")
df_list = [df[i:i+20] for i in range(0, len(df), 20)]
growthData = ""
growthData = pd.DataFrame(columns=['date', 'balance'])

prepareFolders()
startDate = "12/01/2016"   
monthConfig = 1 
wallet = 1000
temp = ''
counter = True
for i  in df_list:
    startDate = pd.to_datetime(startDate)
    startDate = startDate + pd.DateOffset(months=monthConfig)
    startDate = startDate.strftime("%m/%d/%Y")
    i = i.drop(['Field1', 'Field2_links', 'Field4', "Field2_text"], axis=1)
    if counter:
        temp = balanceFund(i,wallet)
        counter = False
        print("this not included",startDate)
    else:
        wallet = calcHoldings(i)
        print(wallet)
        growthData = growthData.append({'date': startDate, 'balance': wallet}, ignore_index=True)
        temp = balanceFund(i,wallet)

growthData.to_csv("growthData.csv", index=False)
plotData = growthData.set_index('date')
plotData.plot()

