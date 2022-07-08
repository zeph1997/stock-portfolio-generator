import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from datetime import datetime, date, timedelta
from pandas_datareader import data, test
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from pmdarima.arima import auto_arima
import RoboFund.lstm as lstm
import math

# stockList: (List) of stocks returned by the screener. 1D list with just the tickers
# timeHorizon: (int) days the Asset Manager intends to hold the stock 
def get_predictions(stockList, timeHorizon):
    outputList = [] # contains tuples with the stock ticker as well as predicted growth in the next <time horizon>
    predictedValues = {}
    start_date = (date.today() - timedelta(days=660)).strftime("%Y-%m-%d") #1825 days, we cannot train too far back, affects data
    end_date = date.today().strftime("%Y-%m-%d")

    df = data.DataReader(stockList,'yahoo', start_date, end_date).fillna(0)
    # df['Date'] = df.index
    # df.reset_index(drop=True, inplace=True)
    df = df["Adj Close"].copy()
    train_data, test_data = df[0:int(len(df)*0.7)], df[int(len(df)*0.7):]
    print(df)

    for i in df:
        training_data = train_data[i].values
        testing_data = test_data[i].values
        history = [x for x in training_data]
        N_test_observations = len(testing_data)
        # Monthly seasonality
        model_autoArima = auto_arima(training_data, start_p=0, start_q=0, test='adf', max_p=5, max_q=5, m=12, d=2, seasonal=True, start_P=0, D=0, trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
        output = model_autoArima.predict(N_test_observations)
        # model = ARIMA(training_data, order=(1, 1, 0))  
        # fitted = model.fit()
        # fc = fitted.forecast(126, alpha=0.05)
        # print(fc)
        MSE_error = mean_squared_error(testing_data, output)

        if False: #(math.sqrt(MSE_error)/testing_data[-1]) < 0.5: 
            # all_data = training_data + testing_data
            #expected_price = model_autoArima.predict(N_test_observations + timeHorizon)
            expected_price = model_autoArima.predict(timeHorizon)
            #expected_price = model.forecast(N_test_observations + timeHorizon,alpha=0.05)
            print(f"Expected Price of {i}: {expected_price[-1]}")
            outputList.append((i,(expected_price[-1]-testing_data[-1])/testing_data[-1]))
            print((i,(expected_price-testing_data[-1])/testing_data[-1]))
            predictedValues[i] = expected_price.tolist()
        else:
            # use other model
            #try:
            print("Fail ARIMA, using LSTM")
            # expected_price = lstm.get_predictions(i,timeHorizon)
            # print(f"Expected Price of {i}: {expected_price[-1]}")
            # outputList.append((i,(expected_price[-1]-testing_data[-1]).item()/testing_data[-1].item()))
            # print((i,(expected_price-testing_data[-1])/testing_data[-1]))
            # predictedValues[i] = expected_price
            # except:
            #     expected_price = model_autoArima.predict(timeHorizon)
            #     #expected_price = model.forecast(N_test_observations + timeHorizon,alpha=0.05)
            #     print(f"Expected Price of {i}: {expected_price[-1]}")
            #     outputList.append((i,(expected_price[-1]-testing_data[-1])/testing_data[-1]))
            #     print((i,(expected_price-testing_data[-1])/testing_data[-1]))
            #     predictedValues[i] = expected_price.tolist()

    print("outlist")
    print(outputList)
    print(predictedValues)
    return sorted(outputList,key=lambda x: x[1],reverse=True),predictedValues
        