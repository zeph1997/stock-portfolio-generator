import datetime as dt
from typing import final
from pandas_datareader import data
import pandas
import numpy as np
from collections import defaultdict

def compare_moving_average(tickerList):
    """Returns a string. If the stock is below moving average, it will be included in the return string"""
    out_dict = {}
    message = ""
    end = dt.date.today()
    start = end-dt.timedelta(days=365)
    tickers = [x[0] for x in tickerList]
    stockdf = data.DataReader(tickers,'yahoo',start,end)
    stockdf.reset_index(inplace=True)
    stockdf = stockdf["Adj Close"]
    final_dict = {}
    for i in tickers:
        final_dict[i] = {'200ma':stockdf[i].rolling(window=200,min_periods=0).mean().iloc[-1],'100ma':stockdf[i].rolling(window=100,min_periods=0).mean().iloc[-1],"50ma":stockdf[i].rolling(window=50,min_periods=0).mean().iloc[-1]}
    for i,j in tickerList:
        print(i,j)
        message += f"{i}:\nCurrent price - ${j}\n"
        indMessage = ""
        if j < final_dict[i]["50ma"]:
            print("Price",j,"50MA:",final_dict[i]["50ma"])
            diff = final_dict[i]["50ma"] - j
            indMessage += f"Current price lower than 50 day MA of ${final_dict[i]['50ma']:.2f} by ${diff:.2f} ({(diff/j) * 100:.2f}%)\n"
        if j < final_dict[i]["100ma"]:
            print("Price",j,"100MA:",final_dict[i]["100ma"])
            diff = final_dict[i]['100ma'] - j
            indMessage += f"Current price lower than 100 day MA of ${final_dict[i]['100ma']:.2f} by ${diff:.2f} ({(diff/j) * 100:.2f}%)\n"
        if j < final_dict[i]["200ma"]:
            print("Price",j,"200MA:",final_dict[i]["200ma"])
            diff = final_dict[i]['200ma'] - j
            indMessage += f"Current price lower than 200 day MA of ${final_dict[i]['200ma']:.2f} by ${diff:.2f} ({(diff/j) * 100:.2f}%)\n"
        message += indMessage + "\n" if indMessage else "Current price is above moving averages.\n\n"
        if indMessage:
            out_dict[i] = f"{i}:\nCurrent price - ${j}\n" + indMessage
    return message, out_dict

def get_stochastic_value(tickerList):
    '''Formula for stochastics
    ( (C - L14) / (H14 - L14) ) * 100
    C = The most recent closing price
    L14 = The lowest price traded of the 14 previous sessions
    H14 = The highes price traded of the same 14 previous sessions
    '''
    out_dict = {}
    message = ""
    end = dt.date.today()
    start = end-dt.timedelta(days=30)
    tickers = [x[0] for x in tickerList]
    stockdf = data.DataReader(tickers,'yahoo',start,end)
    stockdf.reset_index(inplace=True)
    for i,j in tickerList:
        print(i,j)
        message += f"{i}:\nCurrent price - ${j}\n"
        indMessage = ""
        stockdf = stockdf.iloc[-14:,:]
        low = stockdf['Low'][i].min()
        high = stockdf['High'][i].max()
        stoch = ((j - low)/(high - low)) * 100
        if stoch < 20:
            indMessage += f"Stock is OVERSOLD with stochastic value of {stoch:.2f}\n"
            out_dict[i] = f"{i}:\nCurrent price - ${j}\n" + indMessage
        elif stoch < 80:
            indMessage += f"Stock is between stochastic range with a value of {stoch:.2f}\n"
        else:
            indMessage += f"Stock is OVERBOUGHT with stochastic value of {stoch:.2f}\n"
        message += indMessage + "\n"
        
    return message, out_dict

#not sure how you want yourlist to be but i ususally think of it as ['ADBE','APPL','BABA','BOC']
#this is the base form we might have to adjust to 'smoothen it' further
def get_rsi_value(tickerList):
    ''' 
    RSI = 100 – 100 / ( 1 + RS )
    RS = Relative Strength = AvgU / AvgD
    AvgU = average of all up moves in the last N price bars
    AvgD = average of all down moves in the last N price bars
    N = the period of RSI
    '''
    out_dict = {}
    end = dt.date.today()
    start = end-dt.timedelta(days=365)
    message = ""
    tickers = [x[0] for x in tickerList]
    stockdf = data.DataReader(tickers,'yahoo',start,end)
    stockdf.reset_index(inplace=True)
    stockdf = stockdf["Adj Close"]
    for i,_ in tickerList:
        print(i)
        diff = list(stockdf[i].diff())
        oldup = 0
        olddown = 0
        avgup=0
        avgdown=0
        rsi = 0
        for x in range(1,15):
            if(diff[x] > 0):
                print("up:",diff[x])
                avgup += diff[x]
            else:
                print("down:",diff[x])
                avgdown += abs(diff[x])
        oldup = avgup/14
        olddown = avgdown/14
        for z in range(1,len(diff)-14):
            oldup = (oldup * 13 + max(0,diff[z+14]))/14
            olddown = (olddown * 13 + abs(min(0,diff[z+14])))/14
        rsi = 100 - 100/(1 + oldup / olddown)
        message += f"The RSI value for {i} is {rsi:.2f}\n\n"
        out_dict[i] = f"{rsi:.2f}"
    return message,out_dict

def compare_expo_moving_average(tickerList):
    """Returns a string. If the stock is below moving average, it will be included in the return string"""
    tickers = [x[0] for x in tickerList]
    message = ""
    end = dt.date.today()
    start = end-dt.timedelta(days=365)
    stockdf = data.DataReader(tickers,'yahoo',start,end)
    stockdf.reset_index(inplace=True)
    stockdf = stockdf["Adj Close"]
    print(stockdf)
    final_dict = {}
    out_dict = {}
    for i in tickers:
        final_dict[i] = {'50ema':stockdf[i].ewm(span=50).mean().iloc[-1],'100ema':stockdf[i].ewm(span=100).mean().iloc[-1]}
    
    for i,j in tickerList:
        print(i,j)
        message += f"{i}:\nCurrent price - ${j}\n"
        indMessage = ""
        if j < final_dict[i]['50ema']:
            print("Price",j,"50ema:",final_dict[i]['50ema'])
            diff = final_dict[i]['50ema'] - j
            indMessage += f"Current price lower than 50 day EMA of ${final_dict[i]['50ema']:.2f} by ${diff:.2f} ({(diff/j) * 100:.2f}%)\n"
        if j < final_dict[i]['100ema']:
            print("Price",j,"100ema:",final_dict[i]['100ema'])
            diff = final_dict[i]['100ema'] - j
            indMessage += f"Current price lower than 100 day EMA of ${final_dict[i]['100ema']:.2f} by ${diff:.2f} ({(diff/j) * 100:.2f}%)\n"
        message += indMessage + "\n" if indMessage else f"Current price is above moving averages.\n\n"
        if indMessage:
            out_dict[i] = f"{i}:\nCurrent price - ${j}\n" + indMessage
    return message,out_dict

def get_best_stocks(ma_results,ema_results,stoch_results,rsi_results):
    return

def get_refined_stocks(tickerList):
    print("Getting moving averages...")
    message, ma_results = compare_moving_average(tickerList)
    print(">>> " + message)
    #print("Getting exponential moving averages...")
    #message, ema_results = compare_expo_moving_average(tickerList)
    #print(">>> " + message)
    #print("Getting stochastics...")
    #message, stoch_results = get_stochastic_value(tickerList)
    #print(">>> " + message)
    # print("Getting rsi...")
    # message, rsi_results = get_rsi_value(tickerList)

    return [x for x in ma_results]

def get_good_metrics(resultsList):
    temp_dict = defaultdict(int)

    for i in resultsList:
        for j in i:
            temp_dict[j] += 1
    print(temp_dict)
    return [i for i,j in temp_dict.items() if j >= 2]