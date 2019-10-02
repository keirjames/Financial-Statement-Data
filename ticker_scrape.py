import pandas as pd
from bs4 import BeautifulSoup
import requests


def scrape_index_tickers(url, ticker_col):
    # Create BS object using the HTML source code returned by requests.get(url)
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')

    # Isolate the Wikipedia table containing index company tickers
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Scrape the tickers
    tickers = [row.find_all('td')[ticker_col].text.strip('\n') for row in table.find_all('tr')[1:]]
    return tickers


def fetch_all_tickers(index_dict):
    # List for all the tickers from every index to be appended to
    all_tickers = []

    # Iterate through the index dictionary to scrape all tickers using scrape_index_tickers
    for key in index_dict:
        values = index_dict[f'{key}']
        url = values[0]
        ticker_col = values[1]
        tickers = scrape_index_tickers(url, ticker_col)

        # Add tickers from that index into the master ticker list
        for ticker in tickers:
            # Check it's not a duplicate NYSE ticker
            if 'NYSE' not in ticker:
                all_tickers.append(ticker)

    return (pd.Series(all_tickers)).drop_duplicates()