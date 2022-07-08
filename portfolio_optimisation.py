import pandas as pd
import numpy as np
from pandas_datareader import data, wb
import datetime as dt
import scipy.optimize as sco
from scipy import stats

import matplotlib.pyplot as plt

def optimise_portfolio(tickers,predicted_values,risk_appetite,expected_annualised_gains):
    end = dt.date.today()
    start = end-dt.timedelta(days=365)
    print(tickers)
    # df = data.DataReader([x[0] for x in tickers], 'yahoo', start, end)
    # df = df['Adj Close']
    get_selected_columns = {}
    for i in tickers:
        get_selected_columns[i[0]] = predicted_values[i[0]]
    df = pd.DataFrame.from_dict(get_selected_columns)
    print(">>> df")
    print(df)
    # print(">>df_mine")
    # print(df_mine)
    # df.columns = tickers
    only_tickers = [x[0] for x in tickers]
    optimised_port = ""
    
    # Parameters (To edit)
    mean_returns = df.pct_change().mean()
    # print(mean_returns)
    cov = df.pct_change().cov()
    num_portfolios = 10000
    rf = 0.025
    # risk_appetite = 6
    expected_annualised_gains = expected_annualised_gains / 100

    # Calculate annualised return, sd and sharpe ratio of a portfolio
    def calc_portfolio_perf(weights, mean_returns, cov, rf):
        portfolio_return = np.sum(mean_returns * weights) * 252
        portfolio_std = np.sqrt(
            np.dot(weights.T, np.dot(cov, weights))) * np.sqrt(252)
        sharpe_ratio = (portfolio_return - rf) / portfolio_std
        return portfolio_return, portfolio_std, sharpe_ratio

    # Generate portfolios with random weights


    def simulate_random_portfolios(num_portfolios, mean_returns, cov, rf):
        results_matrix = np.zeros((len(mean_returns)+3, num_portfolios))
        for i in range(num_portfolios):
            weights = np.random.random(len(mean_returns))
            weights /= np.sum(weights)
            portfolio_return, portfolio_std, sharpe_ratio = calc_portfolio_perf(weights, mean_returns, cov, rf)
            results_matrix[0, i] = portfolio_return
            results_matrix[1, i] = portfolio_std
            results_matrix[2, i] = sharpe_ratio
            # iterate through the weight vector and add data to results array
            for j in range(len(weights)):
                results_matrix[j+3, i] = weights[j]

        results_df = pd.DataFrame(results_matrix.T, columns=[
                                'ret', 'stdev', 'sharpe'] + [ticker for ticker in only_tickers])

        return results_df


    def get_optimised_port(optimised_port):
        # Simulation Result
        results_frame = simulate_random_portfolios(
            num_portfolios, mean_returns, cov, rf)

        # Locate position of portfolio with highest Sharpe Ratio
        max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]

        # Locate positon of portfolio with minimum standard deviation
        min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

        # get midpoint of variance and find the highest sharpe ratio which is along the efficient frontier
        diff = max_sharpe_port['stdev'] - min_vol_port['stdev']
        diff_half = diff/2
        balance_std = diff_half + min_vol_port['stdev']
        staging =  results_frame[(results_frame['stdev'] > balance_std) & (results_frame['stdev'] < (balance_std + diff_half * 0.2))]
        if not(staging.empty):
            staging = results_frame.iloc[staging['sharpe'].idxmax()]

        #  Recommended portfolio and weightage
        # for aggressive portfolio
        if (risk_appetite > 7 and max_sharpe_port['ret'] >= expected_annualised_gains):
            optimised_port = max_sharpe_port
        
        # for balanced portfolio
        elif (not(staging.empty) and risk_appetite > 3 and staging['ret'] >= expected_annualised_gains):
            optimised_port = staging
        
        # for conservative portfolio
        # if cannot find balanced portfolio, go back to conservative 
        elif (risk_appetite > 0 and min_vol_port['ret'] >= expected_annualised_gains):
            optimised_port = min_vol_port
            
        else:
            optimised_port = ""

        # include this if you want to run an interactive cell
        # Scatter Plot
        # plt.subplots(figsize=(15,10))
        # plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
        # plt.xlabel('Standard Deviation')
        # plt.ylabel('Returns')
        # plt.colorbar()

        # # Red Star: highest Sharpe Ratio
        # plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=500)

        # # Green star: minimum variance portfolio
        # plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='g',s=500)
        # plt.show()

        return optimised_port

    # Run optimisation function till portfolio satsifies both risk appetite and expected annualised gain
    print(">>> Start")

    for i in range(10):
        if (isinstance(optimised_port, str) and optimised_port == ""):
            print(">>> Portfolio optimisation in progress")
            optimised_port = get_optimised_port(optimised_port)
        else:
            break

    if (not(isinstance(optimised_port, str)) and not(optimised_port.empty)):
        print("Here is your optimised portfolio:\n")
        for ticker in only_tickers:
            print(ticker + ": " + str(optimised_port[ticker].round(3)))
        optimised_port = optimised_port.to_dict()
        return optimised_port
        print("\nThis portfolio is expected to have a " +
            str(optimised_port['ret'].round(2)) + "% annualised gain!")
    else:
        return {"sharpe":"No portfolio found", "ret":"No portfolio found"}
