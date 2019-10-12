import ticker_scrape
import ticker_api

# FOR TICKER_SCRAPE: Index List Info Dictionary (key = index ticker) (values = [index_urls_dict, ticker_col in table])
index_urls_dict = {'SPX': ['https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 0],
                   'DJI': ['https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average', 2],
                   'NDAQ': ['https://en.wikipedia.org/wiki/NASDAQ-100#Components', 1]}

# FOR GET DATA: List containing each financial statement type
financialtypes = ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']


# 1 <-- GENERATE TICKERS -->
# 1.1 Generate a Series containing tickers available through API
tickers_api = ticker_api.Tickers(include_stock_names=False).generate_tickers()['Ticker']

# 1.2 Generate a list of tickers scraped from US Stock Indexes in the index_urls_dict
tickers_scrape_indexes = ticker_scrape.fetch_all_tickers(index_urls_dict)


