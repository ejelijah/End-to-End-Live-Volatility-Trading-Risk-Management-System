import yfinance as yf
import pandas as pd
import numpy as np

def get_option_chain(ticker_symbol):
    print(f"Fetching data for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    
    # Get the nearest expiration date
    expirations = ticker.options
    target_date = expirations[0] 
    
    # Get call options for that date
    opt = ticker.option_chain(target_date)
    calls = opt.calls
    
    # We only want liquid options (narrow bid-ask spread)
    calls = calls[calls['volume'] > 10].copy()
    
    # Calculate Mid-Price (The fair market value)
    calls['mid_price'] = (calls['bid'] + calls['ask']) / 2
    
    # Get current stock price
    current_price = ticker.history(period="1d")['Close'].iloc[-1]
    
    print(f"Success! Pulled {len(calls)} liquid strikes for {target_date}")
    return current_price, calls, target_date

if __name__ == "__main__":
    S, data, date = get_option_chain("AAPL")
    # Save to your new data folder
    data.to_csv(f"data/raw/AAPL_{date}_options.csv")
    print(f"Data saved to data/raw/AAPL_{date}_options.csv")