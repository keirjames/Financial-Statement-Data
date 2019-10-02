import ticker_scrape


# FOR TICKER SCRAPE: Index List Info Dictionary (key = index ticker) (values = [index_urls_dict, ticker_col in table])
index_urls_dict = {'SPX': ['https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 0],
                   'DJI': ['https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average', 2],
                   'NDAQ': ['https://en.wikipedia.org/wiki/NASDAQ-100#Components', 1]}


# 1 Scrape tickers for all stock indexes in the index_urls_dict
tickers = ticker_scrape.fetch_all_tickers(index_urls_dict)
