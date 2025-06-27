import yfinance as yf
import pandas as pd  # imported libs

def fetch_stock_data(ticker, period="6mo", interval="1d"):  # this func I created to fetch the stock data
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=False)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [' '.join(col).strip() for col in data.columns.values]

    clean_cols = {} # dic to hold cleaned column names
    for col in data.columns: # iterate ech colmn
        if isinstance(col, tuple):
            col = col[0]
        if '.' in col:
            clean_cols[col] = col.split('.')[0] #splitted the colmn names
        else:
            clean_cols[col] = col
    data.rename(columns=clean_cols, inplace=True) # rename the columns

    if 'Close' not in data.columns: # close colmn is not present
        close_col = [col for col in data.columns if 'Close' in col]
        if close_col:
            data['Close'] = data[close_col[0]]

    return data