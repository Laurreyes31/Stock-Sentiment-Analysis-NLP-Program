import requests
from textblob import TextBlob
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

API_KEY = 'fb2a1428aamsh631a62e9561b826p15d1e4jsn183d90751a2a'

def get_stock_price(ticker):
    url = f"https://mboum-finance.p.rapidapi.com/qu/quote?symbol={ticker}"
    headers = {
        'x-rapidapi-host': "mboum-finance.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_historical_prices(ticker):
    url = f"https://mboum-finance.p.rapidapi.com/hi/history?symbol={ticker}&interval=1d"
    headers = {
        'x-rapidapi-host': "mboum-finance.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_news(ticker):
    url = f"https://mboum-finance.p.rapidapi.com/ne/news?symbol={ticker}"
    headers = {
        'x-rapidapi-host': "mboum-finance.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
    except ValueError:
        return date_str

def create_charts(stock_data, news_sentiments):
    dates = []
    prices = []
    if stock_data:
        dates = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d') for ts in stock_data.get('timestamp', [])]
        prices = stock_data.get('close', [])

    sentiment_dates = [datetime.strptime(article['date_time'].split(' UTC')[0], '%Y-%m-%d %H:%M:%S') for article in news_sentiments]
    sentiments = [float(article['sentiment']) for article in news_sentiments]

    # Plot the stock prices chart
    plt.figure(figsize=(12, 6))
    plt.plot(dates, prices, label='Stock Price', marker='o', linestyle='-', color='tab:blue')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Closing Prices Over Time')
    plt.grid(True)

    # Show the price chart
    plt.show()

    # Convert to Pandas DataFrame
    df = pd.DataFrame({'Date': sentiment_dates, 'Sentiment': sentiments})

    # Group by date to calculate net sentiment per day
    daily_sentiment = df.groupby('Date')['Sentiment'].sum().reset_index()

    # Plot the sentiment scores chart
    plt.figure(figsize=(12, 6))

    # Plot bars with spacing between them
    plt.bar(daily_sentiment['Date'], daily_sentiment['Sentiment'], color=daily_sentiment['Sentiment'].apply(lambda x: 'green' if x > 0 else 'red'), width=0.4)

    # Add labels and title
    plt.xlabel('Date Time')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Scores Over Time')
    plt.ylim([-1, 1])
    plt.grid(True)

    # Show the sentiment chart
    plt.show()

def main():
    ticker = input("Enter the stock ticker symbol: ").strip().upper()

    stock_data = get_historical_prices(ticker)
    news_data = get_news(ticker)

    news_sentiments = []
    if 'body' in news_data:
        for article in news_data['body']:
            content = article.get('title', '')
            date_time = format_date(article.get('pubDate', ''))
            sentiment = analyze_sentiment(content)
            if sentiment != 0:  # Include only non-zero sentiment scores
                news_sentiments.append({
                    'content': content,
                    'date_time': date_time,
                    'sentiment': f"{sentiment:.3f}"  # Format sentiment to 3 decimal places
                })

    create_charts(stock_data, news_sentiments)

    # Calculate average sentiment
    avg_sentiment = sum(float(article['sentiment']) for article in news_sentiments) / len(news_sentiments) if news_sentiments else 0

    print(f"Average Sentiment Score: {avg_sentiment:.3f}")

    # Make a simple recommendation based on sentiment
    if avg_sentiment > 0.1:
        print("Recommendation: Consider buying.")
    elif avg_sentiment < -0.1:
        print("Recommendation: Consider selling.")
    else:
        print("Recommendation: Hold or further analysis needed.")

if __name__ == "__main__":
    main()
