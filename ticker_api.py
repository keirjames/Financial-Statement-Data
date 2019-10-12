import json
from urllib.request import urlopen
import pandas as pd


class Tickers():
    """
    Generate the APIs list of all available tickers.
     '--> Default settings ignore the associated stock names.
    """
    # API address
    url = 'https://financialmodelingprep.com/api/v3/company/stock/list'

    def __init__(self, include_stock_names=False):
        self.include_stock_names = include_stock_names

    def __repr__(self):
        if self.include_stock_names:
            return f"Tickers(include_stock_names=True)"
        else:
            return f"Tickers(include_stock_names=False)"

    def parse_ticker_json(self):
        # Connect with API & return a list of dictionaries (dict for each ticker available)
        response = urlopen(self.url)
        data = response.read().decode('utf-8')
        return json.loads(data)['symbolsList']

    def generate_tickers(self):
        # Generate a DataFrame with the ticker symbols & stock names from the parse_ticker_json() dictionary list
        if self.include_stock_names:
            data = [(ticker_dict['symbol'], ticker_dict['name']) for ticker_dict in self.parse_ticker_json()]
            return pd.DataFrame(data, columns=['Ticker', 'Stock Name'])

        # Generate a DataFrame with the ticker symbols only
        else:
            data = [ticker_dict['symbol'] for ticker_dict in self.parse_ticker_json()]
            return pd.DataFrame({'Ticker': data})