import requests

def send_telegram_alert(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage" # Telegram API endpoint for sending messages
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)
