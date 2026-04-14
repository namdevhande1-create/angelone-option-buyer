import time
import pyotp
import requests
import pandas as pd
import pandas_ta as ta
from SmartApi import SmartConnect

# --- CONFIGURATION (Tumche Details Ithe Taka) ---
API_KEY = "Qs18caYn"
CLIENT_ID = "N358730"
PASSWORD = "1810"
TOTP_SECRET = "OZ5TOT34Z6WGMG4IWX54V6CZJE"
TELEGRAM_BOT_TOKEN = "8672904294:AAFnxOsXP-oPcH_gEACKHrGxZfOgvAZo-yg"
TELEGRAM_CHAT_ID = "5153484923"

# --- FUNCTIONS ---
def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    requests.get(url)

def get_signal(df):
    # 1. VWAP Calculation
    df['vwap'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    
    # 2. 9 EMA Calculation
    df['ema9'] = ta.ema(df['close'], length=9)
    
    # 3. Volume Average (Maagchya 10 candles)
    avg_volume = df['volume'].tail(10).mean()
    
    # Latest Data
    current_price = df['close'].iloc[-1]
    current_volume = df['volume'].iloc[-1]
    current_vwap = df['vwap'].iloc[-1]
    current_ema = df['ema9'].iloc[-1]
    day_high = df['high'].max()

    # --- LOGIC ---
    # Price VWAP ani EMA chya var pahije + Volume spike pahije
    if current_price > current_vwap and current_price > current_ema:
        if current_volume > (avg_volume * 1.5):
            return f"🚀 BREAKOUT! \nPrice: {current_price}\nAbove VWAP & 9EMA\nVolume is High!"
    
    return None

# --- MAIN EXECUTION ---
obj = SmartConnect(api_key=API_KEY)
session = obj.generateSession(CLIENT_ID, PASSWORD, pyotp.TOTP(TOTP_SECRET).now())

if session['status']:
    send_telegram_msg("✅ Algo Alert System Started!")
    while True:
        try:
            # Ithe apun Nifty cha 5-min data fetch karu (Simplified Logic)
            # Real API call sathi obj.getCandleData vaprave lagel
            
            # Kalpanik data (Example sathi)
            # df = get_live_data_from_angel() 
            
            # signal = get_signal(df)
            # if signal:
            #    send_telegram_msg(signal)
            
            time.sleep(60) # Dar ek minitane check karel
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
else:
    print("Login Failed!")
