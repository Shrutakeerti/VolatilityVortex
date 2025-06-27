import pandas as pd

def compute_rsi(series, period=14): # Relative Strength Index
    if isinstance(series, pd.DataFrame):
        series = series.iloc[:, 0]  # con df to series
    delta = series.diff() # diff b/w consec val
    gain = delta.clip(lower=0) # + changes
    loss = -1 * delta.clip(upper=0) # - changes
    avg_gain = gain.rolling(period).mean() # avg of + changes
    avg_loss = loss.rolling(period).mean() # avg of - changes
    rs = avg_gain / avg_loss # relative strength
    rsi = 100 - (100 / (1 + rs)) # RSI formula
    return rsi

def compute_dma(data, short_window=20, long_window=50): #daily mov avgs
    data['20DMA'] = data['Close'].rolling(window=short_window).mean() # 20 day mov avgs
    data['50DMA'] = data['Close'].rolling(window=long_window).mean() # 50 day mov avgs
    return data

def generate_signals(df): # gen buy sig 
    signals = []
    for i in range(1, len(df)): # start from inx 1 so that I can avoid NaN for the first row
        row = df.iloc[i] # current row (iloc for loc based indexing)
        prev = df.iloc[i - 1] # prev row

        rsi = row['RSI'] # RSI val
        dma20 = row['20DMA'] 
        dma50 = row['50DMA']
        prev_dma20 = prev['20DMA']
        prev_dma50 = prev['50DMA']
        close = row['Close']

        if not any(pd.isna([rsi, dma20, dma50, prev_dma20, prev_dma50])): # check for NaN
            print(f"📊 {df.index[i].date()} | RSI: {rsi:.2f} | 20DMA: {dma20:.2f} | 50DMA: {dma50:.2f}")
          
            if (rsi < 50) and (dma20 > dma50): # buy condition as mentioned in PS
                signals.append((df.index[i], 'BUY', close))

    if not signals:
        print("⚠ No signals met the conditions.")

    return signals
