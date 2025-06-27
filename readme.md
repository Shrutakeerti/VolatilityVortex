# 🚀 Algo-Trading System with ML, Automation, and Live Alerts

> An end-to-end algorithmic trading prototype built with Python, powered by RSI + DMA strategy, enhanced with ML predictions, Google Sheets P&L tracking, Groq commentary, and Telegram alerts — all wrapped in a stylish Flask UI.

---

## 🔧 Tech Stack

| Component         | Stack / Tool                       |
|------------------|-------------------------------------|
| Strategy Logic   | RSI + 20DMA / 50DMA Crossover       |
| ML Model         | Scikit-Learn (Decision Tree)        |
| Stock Data       | Yahoo Finance via `yfinance`        |
| Automation       | Python + Flask                      |
| Logging & P&L    | Google Sheets API + GCP Service     |
| Alerts           | Telegram Bot API                    |
| Commentary       | Groq API (LLaMA3-70B Instruct)      |
| UI               | HTML5 + CSS3 (Glassmorphism style)  |

---

## 📈 Strategy Logic

This project implements a hybrid **technical + rule-based strategy**:

- ✅ **Buy Signal Conditions:**
  - **RSI < 30** (oversold)
  - **20DMA crosses above 50DMA**
  - Optional relaxed condition: RSI < 50 + 20DMA > 50DMA (for testing)

- ✅ **Backtest Window:**
  - Last 6 months (`period='6mo'`) using daily candles (`interval='1d'`)

- ✅ **Backtest Output:**
  - Total Trades
  - Win Count / Loss Count
  - Win Ratio
  - Total P&L

---

## 🤖 Machine Learning Automation

- **Model:** `DecisionTreeClassifier`
- **Features Used:**
  - RSI
  - 20DMA
  - 50DMA
  - MACD
  - Volume
- **Target:** Whether next-day close is higher than today’s close
- **Train/Test Split:** 80/20
- **Accuracy Output** is displayed on the UI

---

## ☁️ Google Sheets Logging (via GCP)

Trade and summary logs are stored live using:

- 🔐 A `creds.json` file (GCP Service Account key)
- 📊 Trade logs go to `Trade_Log` sheet
- 📘 Summary stats go to `Summary` tab with:
  - Date
  - Total Trades
  - Wins / Losses
  - Win Ratio
  - P&L

**Libraries Used:**
- `gspread`
- `oauth2client`

---

## 📬 Telegram Alerts

Each trade signal is pushed via **Telegram Bot API** in real-time:

- Uses: `requests.post` to the Telegram API
- Requires:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

> You’ll get alerts like:  
> 📢 `RELIANCE.NS BUY at 2953.25`

---

## 🧠 Groq AI Commentary

Each trading cycle ends with **Groq LLaMA3-based summarization**:

- Model: `llama3-70b-8192`
- API: `https://api.groq.com/openai/v1/chat/completions`
- Output: Smart summary of the day’s trade signals

Example:
> “Today, RELIANCE and TCS showed promising RSI-based buy signals supported by DMA crossovers. INFY remained neutral.”

---

## 💻 Flask UI (Modern 3D-Styled)

### ✅ Features:
- Responsive, animated UI
- Glassmorphism cards
- Color-coded trade signals
- Display of:
  - Trade Signal Table
  - ML Model Accuracy
  - Groq Commentary

### 📸 Preview

![Dashboard Screenshot](https://github.com/Shrutakeerti/VolatilityVortex/tree/main/screenshots)

> UI styled using custom CSS with:
> - `backdrop-filter` + `-webkit-backdrop-filter` for Safari support
> - Neon headings
> - Card animations and hover effects

---

## 🗂️ Project Structure

│
├── app.py # Flask server
├── strategy.py # RSI + DMA logic
├── ml_model.py # Decision Tree model
├── data_fetcher.py # Yahoo Finance fetcher
├── telegram_alert.py # Sends alerts
├── groq_commentary.py # Groq LLM summary
├── google_sheets.py # Google Sheets logging via GCP

│
├── static/
│ └── style.css # UI styling (glassmorphism)
│

├── templates/
│ └── index.html # Frontend dashboard
│

├── creds.json # GCP service account key
└── .env # Secrets (API keys, tokens)

---


## 🔑 Environment Setup

Create a `.env` file with:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_SHEET_NAME=YourSheetName
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🚀 How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the Flask app
python app.py

# Visit the dashboard at:
http://localhost:5000
```


---

### ✅ 10. Demo Videos Section
```markdown
## 📹 Demo Videos

| Demo Type                | Link                         |
|--------------------------|------------------------------|
| 📽️ Strategy & Code Flow | [Watch on Google Drive](#)   |
| 📊 Output + Google Sheets | [Watch on Google Drive](#)  |

```

## ✅ Deliverables Checklist

- ✅ RSI + DMA strategy logic  
- ✅ 6-month backtesting  
- ✅ Decision Tree prediction  
- ✅ Google Sheets automation  
- ✅ Telegram alerts  
- ✅ Groq-generated insights  
- ✅ Modern web UI  
- ✅ Modular, well-documented code  

## 🙌 Author

**Shrutakeerti** — For any updates please contract through the given links 
🔗 [GitHub](https://github.com/Shrutakeerti) &nbsp;&nbsp; 📬 [Telegram](@Shrutakeerti22J10k) &nbsp;&nbsp; 💼 [LinkedIn](https://www.linkedin.com/in/shrutakeerti-datta-872179246/)

## 📃 License

MIT License – use this as a template, study tool, or launchpad for your own bots.

> _“Systems trade logic. Traders trade emotion. Bots don’t care.”_
