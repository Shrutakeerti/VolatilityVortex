from flask import Flask, render_template
from data_fetcher import fetch_stock_data
from strategy import generate_signals, compute_rsi, compute_dma
from ml_model import train_predict
from google_sheets import connect_sheets, log_trade, log_summary
from telegram_alert import send_telegram_alert
from groq_commentary import get_groq_commentary
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

app = Flask(__name__)

@app.route("/")
def index():
    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    all_signals = []
    wins = 0
    losses = 0
    total_pnl = 0

    sheet = connect_sheets(GOOGLE_SHEET_NAME)
    last_ticker_data = None

    for ticker in tickers:
        data = fetch_stock_data(ticker)
        if data.empty or len(data) < 50:
            print(f"⚠ Not enough data for {ticker}. Skipping.")
            continue

        data['RSI'] = compute_rsi(data['Close'])
        data = compute_dma(data)

        signals = generate_signals(data)
        all_signals.extend([(ticker,) + sig for sig in signals])

        for sig in signals:
            log_trade(sheet, [ticker, str(sig[0]), sig[1], sig[2]])
            send_telegram_alert(f"{ticker} {sig[1]} at {sig[2]}", TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

            if sig[1] == "BUY":
                try:
                    next_close = data.loc[sig[0]:].iloc[1]['Close']
                    pnl = next_close - sig[2]
                    total_pnl += pnl
                    if pnl > 0:
                        wins += 1
                    else:
                        losses += 1
                except:
                    pass

        last_ticker_data = data

    total_trades = wins + losses
    win_ratio = (wins / total_trades) if total_trades else 0

    log_summary(sheet, [
        str(datetime.now()),
        total_trades,
        wins,
        losses,
        round(win_ratio, 2),
        round(total_pnl, 2)
    ])

    acc, _ = train_predict(last_ticker_data) if last_ticker_data is not None else ("N/A", None)
    groq_output = get_groq_commentary("Summarize today's trading signals: " + str(all_signals), GROQ_API_KEY)

    return render_template("index.html", signals=all_signals, acc=acc, groq_output=groq_output)

if __name__ == "__main__":
    app.run(debug=True)
