from binance.client import Client
from key import api_key, api_secret
from pandas import DataFrame as df


client = Client(api_key=api_key, api_secret=api_secret)


def get_data(symbol_1,symbol_2,interval,start):
    symbol = symbol_1 + symbol_2
    data = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start)
    frame = df(data)
    return frame