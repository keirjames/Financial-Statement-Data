import time
import numpy as np
from collections import Counter
import pandas as pd
import json
from urllib.request import urlopen


class FinancialStatementData:
    """
    Functionality for creating a multiyear DataFrame for a single ticker and a single financial type.
     '--> Uses the 'years' class attribute list as the benchmark for which years data should be present.
           '--> Handles missing years by adding in dummy rows containing np.nan
    """
    # A list containing the benchmark list of years the data should span over
    years = ['2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009']

    def __init__(self, ticker, ftype):
        # Initialise the instance URL for the specified ticker and financial statement type
        self.ticker = ticker
        self.ftype = ftype
        self.url = f"https://financialmodelingprep.com/api/v3/financials/{ftype}/{ticker}"

    def __repr__(self):
        return f"FinancialStatementData('{self.ticker}', '{self.ftype}')"

    def download_ftype_json(self):
        # Return a dictionary containing that stocks financial type data, with each year as the key
        response = urlopen(self.url)
        data = response.read().decode('utf-8')
        return json.loads(data)['financials']

    @staticmethod
    def duplicate_years(dates_included):
        # Make lists of the years included in the passed dates_included for a multiyear_df
        years_included = [date[0] for date in dates_included]
        # Determine if there are duplicate years in the multiyear_df (eg/ 2016-01-01 & 2016-12-24)
        duplicates = [year for year, count in Counter(years_included).items() if count > 1]

        return True if duplicates else False

    @staticmethod
    def gen_new_years_for_dups(dates_included, years_included):
        # If the most recent year's month is >= June: create new list of years starting from recent year +1
        if int(dates_included[0][1]) >= 6:
            # Return new years based on the new_recent_year end point
            new_recent_year = (int(dates_included[0][0]) + 1)
            return [str(i) for i in range(new_recent_year, new_recent_year - len(years_included), -1)]

        # Else: create a new list of years starting from the last year -1
        else:
            # Return new years based on the new_oldest_year start point
            new_oldest_year = (int(dates_included[0][0]) - 1)
            return [str(i) for i in range(new_oldest_year + len(years_included), new_oldest_year, -1)]

    def ftype_multiyear_df(self):
        # Create DataFrame to append a ticker's data for all years for the specified ftype
        multiyear_df = pd.DataFrame()

        # Iterate through the years in the ftype dictionary produced by download_ftype_json()
        for year in self.download_ftype_json():
            # Create a DataFrame from this year's dictionary
            columns = year.keys()
            rows = year.values()
            yeardf = pd.DataFrame(rows, columns).transpose()
            # Append this year's dictionary to the ticker & ftype's multiyear_df
            multiyear_df = pd.concat([multiyear_df, yeardf], sort=True)

        # What are the dates for the data downloaded in the multiyear_df?
        dates_included = [date.split('-')[0:2] for date in list((multiyear_df['date']))]  # List of (year, month)
        years_included = [date[0] for date in dates_included]  # List of years

        # Does the DataFrame contain any duplicate years?
        # Example: contains 2016-01-01 & 2016-12-24
        # '--> If so then modify the years_included range to account for it & set that as the new 'date' column
        if self.duplicate_years(dates_included):
            years_included = self.gen_new_years_for_dups(dates_included, years_included)
            multiyear_df['date'] = years_included

        # Does the DataFrame contain data for all the years?
        # Yes: Set the index to the 'date' column
        if len(multiyear_df) == len(self.years):
            return multiyear_df.set_index('date')

        # No it doesn't: add np.nan dummy data to fill in the missin years
        else:
            # Calculate which years are missing comparing the 'date' column & the 'years' list
            dates_needed = set(self.years) - set(years_included)

            # Create a DataFrame containing dummy np.nan for the missing years to append to included data
            fill_in_df = pd.DataFrame(np.full(shape=(len(dates_needed), len(multiyear_df.columns)), fill_value=np.nan),
                                      index=list(dates_needed), columns=multiyear_df.columns)
            fill_in_df['date'] = dates_needed

            # Concatenate the incomplete multiyear_df with the dummy full_in_df
            return pd.concat([multiyear_df, fill_in_df], sort=True).set_index('date')


class DataFrameGenerator(FinancialStatementData):
    """
    Functionality for creating a MASTER DataFrame for the specified financial type (ftype), which contains:
        - Data for every ticker, for every year.

    Notes on missing data:
        - If the data for a whole ticker is unavailable, then there will be NaNs for all rows & columns.
        - If the data for a ticker is just missing several years, then the rows will be NaNs.
    """

    def __init__(self, tickers, ftype):
        self.tickers = tickers
        self.ftype = ftype

    def __repr__(self):
        return f"DataFrameGenerator({self.tickers}, '{self.ftype}')"

    def gen_dataframe(self):
        # Generate a list of DataFrames - one for each ticker which contains the ftype data for all years
        df_list = []
        for index, ticker in enumerate(self.tickers):
            try:
                df_list.append(FinancialStatementData(ticker, self.ftype).ftype_multiyear_df())
                print(f'{self.ftype} {index} - SUCCESS - TICKER DATA EXISTS.')
                time.sleep(0.5)
            except:
                print(f'{self.ftype} {index} - FAILURE - LIKELY BAD DATA - Replaced with DataFrame containing NaNs!')
                df_list.append(pd.DataFrame(data=np.nan, index=self.years, columns=df_list[index - 1].columns))

        # Combine all the DataFrames in the list to form a MASTER DataFrame for the specified financial type
        master_df = pd.DataFrame()
        for df in df_list:
            master_df = pd.concat([master_df, df], sort=True)

        # Reset the master_df index and rename the date column
        master_df = master_df.reset_index().rename(columns={'date': 'Date Exact'})

        # Create an appropriate MultiIndex using the list of tickers, and the class variable list of years
        idx = pd.MultiIndex.from_product([self.tickers, self.years], names=['ticker', 'date'])

        # Return the Multidimensional dataframe containing all tickers for all years for a single ftype
        return pd.DataFrame(data=np.array(master_df), index=idx, columns=master_df.columns)