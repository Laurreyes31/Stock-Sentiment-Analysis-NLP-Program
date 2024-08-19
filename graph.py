import yfinance

tsla = yfinance.Ticker('TSLA')
hist = tsla.history(period='1y')

import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(x=hist.index,y=hist['Close'], mode='lines'))
fig.show()