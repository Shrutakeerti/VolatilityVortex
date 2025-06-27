from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from strategy import compute_rsi, compute_dma  # i have used decision tree as model 
def prepare_features(data): # its redefining the fea
    if 'RSI' not in data.columns: # rsi pre or not
        data['RSI'] = compute_rsi(data['Close'])
    data = compute_dma(data)
    if 'MACD' not in data.columns:
        data['MACD'] = data['Close'].ewm(span=12).mean() - data['Close'].ewm(span=26).mean() # taken 26 as def value
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int) #target val

    required_cols = ['RSI', '20DMA', '50DMA', 'MACD'] #required coloumns as per ths PS
    missing_cols = [col for col in required_cols if col not in data.columns] # checking for missing coloumns
    if missing_cols:
        print(f"⚠ Missing columns for model: {missing_cols}")
        return data.iloc[0:0][[]], data.iloc[0:0]

    data = data.dropna(subset=required_cols) #data rows with NaNs
    if data.empty:
        print("⚠ Data empty after dropping NaNs.")
        return data.iloc[0:0][[]], data.iloc[0:0] # returns coloumns but no rows 

    feature_cols = [col for col in ['RSI', '20DMA', '50DMA', 'MACD', 'Volume'] if col in data.columns] # feature columns
    X = data[feature_cols]
    y = data.loc[X.index, 'Target'] # target column
    return X, y

def train_predict(data): # trains the model and predicts
    X, y = prepare_features(data)
    if X.empty or len(X) < 10: # <10 because data needed 
        print("⚠ Not enough data to train.")
        return 0, None

    split = int(0.8 * len(X)) # 8 : 2 ratio split
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = DecisionTreeClassifier() # decision tree model
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    return acc, model
