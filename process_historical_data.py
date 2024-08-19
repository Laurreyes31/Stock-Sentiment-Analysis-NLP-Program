import requests
from datetime import datetime

API_KEY = 'fb2a1428aamsh631a62e9561b826p15d1e4jsn183d90751a2a'  # Replace with your actual API key

def get_historical_prices(ticker):
    url = f"https://mboum-finance.p.rapidapi.com/hi/history?symbol={ticker}&interval=5m"
    headers = {
        'x-rapidapi-host': "mboum-finance.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }
    response = requests.get(url, headers=headers)
    
    # Print out the entire JSON structure for inspection
    data = response.json()
    print("Entire JSON Response:")
    print(data)
    
    if 'data' in data:
        for timestamp, price_data in data['data'].items():
            print(f"Timestamp: {timestamp}, Data: {price_data}")
    
    return data

def create_charts(historical_prices):
    if not historical_prices or 'data' not in historical_prices:
        print("Historical data is missing or improperly parsed.")
        return
    
    dates = []
    closes = []
    
    for timestamp, price_data in historical_prices['data'].items():
        dates.append(datetime.utcfromtimestamp(int(timestamp)))
        closes.append(price_data['close'])
    
    # Now you can use the `dates` and `closes` for plotting
    print("Dates:", dates)
    print("Closing Prices:", closes)

# Example usage
ticker = 'AAPL'  # Replace with the desired ticker
historical_prices = get_historical_prices(ticker)
create_charts(historical_prices)
