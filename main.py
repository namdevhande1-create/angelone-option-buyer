import os
import time
import pyotp
import requests
import pandas as pd
from SmartApi import SmartConnect

# --- CONFIGURATION (Render chya Env Variables madhun ghetlele) ---
API_KEY = os.environ.get('ANGEL_API_KEY')
CLIENT_ID = os.environ.get('ANGEL_CLIENT_ID')
PASSWORD = os.environ.get('ANGEL_PIN')
TOTP_SECRET = os.environ.get('ANGEL_TOTP_SECRET')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 1. Telegram Alert Function
def send_alert(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
        requests.get(url)
    except Exception as e:
        print(f"Telegram Error: {e}")

# 2. EMA Calculation (Pandas-ta chi garaj nahi)
def calculate_ema(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

# 3. SMC Strategy Logic
def check_smc_strategy(df):
    """
    SMC Logic: Order Block + EMA Confirmation
    """
    df['ema9'] = calculate_ema(df, 9)
    df['ema14'] = calculate_ema(df, 14)
    
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Simple Bullish SMC Signal: Last candle was Red, Current is Green 
    # and 9 EMA crossed above 14 EMA (BOS/CHoCH)
    if prev['ema9'] <= prev['ema14'] and last['ema9'] > last['ema14']:
        return "BULLISH_SIGNAL", last['close']
    
    if prev['ema9'] >= prev['ema14'] and last['ema9'] < last['ema14']:
        return "BEARISH_SIGNAL", last['close']
        
    return None, None

# 4. Main Execution Loop
def run_algo():
    try:
        # Angel One Login
        obj = SmartConnect(api_key=API_KEY)
        token = pyotp.TOTP(TOTP_SECRET).now()
        res = obj.generateSession(CLIENT_ID, PASSWORD, token)
        
        if not res['status']:
            send_alert("❌ *Login Failed!* Check your API Credentials.")
            return

        send_alert("🚀 *Algo Live on Render!* Monitoring Market for SMC Signals.")

        while True:
            # Note: Ithe tumhala historical data fetch karnyacha code add karava lagel
            # Sadhyasathi ha loop active rahil
            
            # --- EXAMPLE SIGNAL LOGIC ---
            # signal, price = check_smc_strategy(df)
            # if signal == "BULLISH_SIGNAL":
            #    send_alert(f"✅ *SMC BUY ALERT!* Price: {price} | RR 1:3 Set.")
            
            time.sleep(60) # Dar minitila check karel

    except Exception as e:
        send_alert(f"⚠️ *Algo Error:* {str(e)}")
        time.sleep(300) # Error aala tar 5 min thamba

if __name__ == "__main__":
    run_algo()
