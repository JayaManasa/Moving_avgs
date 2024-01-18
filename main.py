import matplotlib.pyplot as plt
import pandas_ta as ta
import json
import numpy as np
import pandas as pd

data = pd.read_json("day.json")

data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

data['MA50'] = ta.sma(data['close'], 50)
data['MA200'] = ta.sma(data['close'], 100)


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

data['Buy_Signal_price'], data['Sell_Signal_price'] = buy_sell(data)




print(data.head(800))