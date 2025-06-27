import gspread
from oauth2client.service_account import ServiceAccountCredentials # imported thhe libs

def connect_sheets(sheet_name): # func to conn google sheets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope) # creds file to access sheets
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)
    return sheet
TRADE_TAB_CACHE = {} # global val to cache trade_log trab
def log_trade(sheet, trade_data): # func to log trades
    """
    Logs a trade entry into the 'Trade_Log' worksheet.
    """
    global TRADE_TAB_CACHE

    if "trade_log" not in TRADE_TAB_CACHE: # if the trade_log tab is not in cache
        worksheets = sheet.worksheets()
        sheet_titles = [ws.title.strip().lower() for ws in worksheets]
        print(f"📋 Existing sheets: {sheet_titles}")

        if "trade_log" in sheet_titles: # if the trade_log tab is in cache
            trade_tab = next(ws for ws in worksheets if ws.title.strip().lower() == "trade_log")
        else:
            print("📝 Trade_Log not found. Creating it.")
            trade_tab = sheet.add_worksheet(title="Trade_Log", rows="1000", cols="4")
            trade_tab.append_row(["Ticker", "Date", "Signal", "Price"])
        
        TRADE_TAB_CACHE["trade_log"] = trade_tab # cache the trade_log
    else:
        trade_tab = TRADE_TAB_CACHE["trade_log"]

    trade_tab.append_row(trade_data) # append func we all know



def log_summary(sheet, summary_data): # func to log summary
    """
    Logs a summary entry into the 'Summary' worksheet of the Google Sheet.
    If the sheet doesn't exist, it creates it and adds a header row.
    """
    sheet_titles = [ws.title.strip() for ws in sheet.worksheets()]
    print(f"📋 Existing sheets: {sheet_titles}")

    if "Summary" in sheet_titles: # when summary - tab not in cache
        summary_tab = sheet.worksheet("Summary")
    else:
        print("📝 Summary not found. Creating it.")
        summary_tab = sheet.add_worksheet(title="Summary", rows="1000", cols="4")
        summary_tab.append_row(["Date", "RSI", "20DMA", "50DMA"])

    summary_tab.append_row(summary_data) 
