import os
import time
import pyotp
import requests
from SmartApi import SmartConnect

# Keys from Render Environment Variables
API_KEY = os.environ.get('ANGEL_API_KEY')
CLIENT_ID = os.environ.get('ANGEL_CLIENT_ID')
PASSWORD = os.environ.get('ANGEL_PIN')
TOTP_SECRET = os.environ.get('ANGEL_TOTP_SECRET')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(url)

def run_algo():
    try:
        obj = SmartConnect(api_key=API_KEY)
        token = pyotp.TOTP(TOTP_SECRET).now()
        res = obj.generateSession(CLIENT_ID, PASSWORD, token)
        
        if res['status']:
            send_alert("🚀 Algo Live! SMC Strategy Monitoring Started.")
            while True:
                # Basic Loop to keep script alive
                time.sleep(60)
        else:
            send_alert("❌ Login Failed. Check Keys.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_algo()
