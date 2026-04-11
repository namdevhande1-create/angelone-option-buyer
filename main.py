import pyotp
import time
import pandas as pd
import pandas_ta as ta
from SmartApi import SmartConnect

# --- CONFIGURATION ---
API_KEY = "YOUR_API_KEY"
CLIENT_ID = "YOUR_CLIENT_ID"
PASSWORD = "YOUR_TRADING_PIN"
TOTP_SECRET = "YOUR_QR_SECRET_KEY"

# Angel One Connect
obj = SmartConnect(api_key=API_KEY)
token = pyotp.TOTP(TOTP_SECRET).now()
obj.generateSession(CLIENT_ID, PASSWORD, token)

def get_atm_strike(ltp, step=50):
    return round(ltp / step) * step

def identify_order_block(df):
    """
    SMC Logic: Last opposite candle before a strong move.
    """
    last_candle = df.iloc[-1]
    prev_candle = df.iloc[-2]
    
    # Bullish OB: Red candle followed by a big Green candle (BOS)
    if prev_candle['close'] < prev_candle['open'] and last_candle['close'] > prev_candle['open']:
        return "BULLISH_OB", prev_candle['low']
    
    # Bearish OB: Green candle followed by a big Red candle
    if prev_candle['close'] > prev_candle['open'] and last_candle['close'] < prev_candle['low']:
        return "BEARISH_OB", prev_candle['high']
    
    return None, None

def place_smart_order(symbol, side, ltp, sl_points):
    """
    Risk-Reward 1:3 Logic
    """
    target_points = sl_points * 3
    print(f"Executing {side} Order | Entry: {ltp} | SL: {ltp-sl_points} | Target: {ltp+target_points}")
    
    # Angel One Order Placement Logic Ithe Yeil
    # obj.placeOrder(...) 

def run_smc_algo():
    print("SMC Algo Started... Searching for Order Blocks.")
    while True:
        # 1. Fetch Nifty/Sensex Data (5 min)
        # df = get_historical_data("NIFTY") 
        
        # 2. SMC Check
        ob_type, ob_level = identify_order_block(df)
        ltp = df.iloc[-1]['close']
        
        if ob_type == "BULLISH_OB":
            atm = get_atm_strike(ltp, 50)
            # Entry point: Near the Order Block level
            if ltp <= ob_level * 1.001: # 0.1% buffer
                sl = 20 # Points in Option
                place_smart_order(f"NIFTY{atm}CE", "BUY", ltp, sl)
                break # Ek trade jhala ki thamba (ki loop suru theva)

        time.sleep(60)

if __name__ == "__main__":
    run_smc_algo()
