import ticker_scrape
import ticker_api
import get_ftype_data

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

# 1.3 Generate a list of the tickers that intersect both the tickers_api & tickers_scrape_indexes
tickers = list(set(tickers_scrape_indexes).intersection(tickers_api))

# 2 <-- GENERATE TICKERS -->
# 2.1 Generate DataFrames for each Financial Statement Type for All Years
income_statement_df = get_ftype_data.DataFrameGenerator(tickers, financialtypes[0]).gen_dataframe()
balance_sheet_df = get_ftype_data.DataFrameGenerator(tickers, financialtypes[1]).gen_dataframe()
cash_flow_df = get_ftype_data.DataFrameGenerator(tickers, financialtypes[2]).gen_dataframe()

# 3 <-- SAVE DATA -->
# 3.1 DataFrame -> CSV
income_statement_df.to_csv('all_income_statement_df.csv')
balance_sheet_df.to_csv('all_balance_sheet_df.csv')
cash_flow_df.to_csv('all_cash_flow_df.csv')
