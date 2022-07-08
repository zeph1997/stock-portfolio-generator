from keras.backend import reverse
import pandas as pd
import numpy as np
from pandas_datareader import data
import datetime as dt

def get_cross_corr():
    tickers = ["SPY","XLC","XLY","XLP","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU"]

    start_date= str(dt.date.today() - dt.timedelta(days = int(365*1)))
    end_date = str(dt.datetime.today())

    panel_data = data.DataReader(tickers,'yahoo', start_date, end_date)['Adj Close']

    part = get_top_abs_correlations(panel_data)

    return part


def get_cross_corr_gold_bond():
    tickers = ["SPY","XLC","XLY","XLP","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU"]

    start_date= str(dt.date.today() - dt.timedelta(days = int(365*1)))
    end_date = str(dt.datetime.today())

    panel_data = data.DataReader(tickers,'yahoo', start_date, end_date)['Adj Close']

    main_corr_tickers = ["GDX","TLT"]

    shift_data = data.DataReader(main_corr_tickers,'yahoo', start_date, end_date)['Adj Close']
    panel_data_shifted = panel_data.shift(periods=3,fill_value=0).copy()

    completed_time_shifted = pd.concat([shift_data,panel_data_shifted],axis=1)


    # print('\nCorrelation Matrix')
    corr_matrix = completed_time_shifted.corr()
    # corr_matrix.to_csv(f"cross_corr_matrixtest.csv")

    def get_top_abs_correlations_special(df):
        au_corr = df.corr().unstack()
        au_corr = au_corr[["GDX","TLT"]]
        # labels_to_drop = get_redundant_pairs(df)
        labels_to_drop = set()
        labels_to_drop.add(('GDX','GDX'))
        labels_to_drop.add(('TLT','TLT'))
        labels_to_drop.add(('GDX','TLT'))
        au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
        au_corr.to_csv(f"cross_corr_top_abs_corrtest.csv")
        return au_corr

    # print("\nTop Absolute Correlations")
    a = get_top_abs_correlations_special(completed_time_shifted).to_dict()
    out = []
    for i,j in a.items():
        out.append([i,j])
    
    return sorted(out,key=lambda x:abs(x[1]),reverse=True)

def get_top_abs_correlations(df):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    au_corr.to_csv(f"cross_corr_top_abs_corrtest.csv")
    return au_corr

def get_redundant_pairs(df):
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop