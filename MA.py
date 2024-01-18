import pandas as pd
import json
import pandas_ta as ta
import numpy as np


data = pd.read_json('day.json')
data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

data['MA50'] = data.ta.sma(50)
data['MA200'] = data.ta.sma(200)


def buy_sell(data):
    signalBUY = []
    signalSELL = []
    position = False

    for i in range(len(data)):
        if data['MA50'][i] > data['MA200'][i]:
            if position == False :
                signalBUY.append(data['close'][i])
                signalSELL.append(np.nan)
                position = True
            else:
                signalBUY.append(np.nan)
                signalSELL.append(np.nan)
        elif data['MA50'][i] < data['MA200'][i]:
            if position == True :
                signalBUY.append(np.nan)
                signalSELL.append(data['close'][i])
                position = False
            else:
                signalBUY.append(np.nan)
                signalSELL.append(np.nan)
        else:
            signalBUY.append(np.nan)
            signalSELL.append(np.nan)
    return pd.Series([signalBUY, signalSELL])


data['Buy_Sell'] = buy_sell(data)


pd.set_option('display.max_rows', None)
print(data.head(2000))

#Calculating cumulative return
data['cumulative_return'] = np.cumsum(data['Buy_Signal_price'])
print(data.head(600))


#Calculate Maximum Drawdown
data['HighValue'] = data['cumulative_return'].cummax()
data['Drawdown'] = data['cumulative_return'] - data['HighValue']

# Calculate annualized return over 3 years
#data['total_return'] = (data['close'][-1] - data['close'][0]) / data['close'][0]
#print(data['total_return'])

#annualized_return = ((1 + data['total_return'])**(1/3))-1


#Calculating sharpe_ratio
sharpe_ratio = data['close'].mean()/data['close'].std()
print("sharpe_ratio is:", sharpe_ratio)

data.to_excel('output.xlsx')