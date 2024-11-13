import json
from datetime import datetime, timedelta

import numpy as np
import yfinance as yf
from model.index import Index
import pandas as pd


class Loader:
    __DEFAULT_LOOKUPS = 365
    __DEFAULT_END = datetime.today()
    __DEFAULT_DATE_FORMAT = '%Y-%m-%d'
    __LINES = '-----------------------------------------------------------'

    def __init__(self, conf_file: str):
        self.indexes: list[Index] = []
        self.__inject_data_from_yahoo(conf_file)
        self.setup_daily_log_return()
        self.setup_volatility()
        pass

    def __inject_data_from_yahoo(self, conf_file):

        try:
            with open(conf_file, 'r') as file_conf:
                config = json.load(file_conf)
                lookup_days = config.get('lookup_days', Loader.__DEFAULT_LOOKUPS)
                end_date = config.get('end_date', Loader.__DEFAULT_END)
                date_format = config.get('date_format', Loader.__DEFAULT_DATE_FORMAT)
                start_date = (end_date - timedelta(days=lookup_days)).strftime(date_format)
                end_date = end_date.strftime(date_format)
                index_list = config.get('indexes', None)
                for index in index_list:
                    from_yahoo = yf.download(
                        index_list[index],
                        start=start_date,
                        end=end_date
                    )
                    from_yahoo = pd.DataFrame({key[0]: value for key, value in from_yahoo.items()})
                    from_yahoo.reset_index(inplace=True)
                    from_yahoo.rename(columns={'index': 'Date'}, inplace=True)
                    from_yahoo.rename(columns={'Adj Close': 'Adjusted Close'}, inplace=True)
                    from_yahoo['Date'] = from_yahoo['Date'].dt.date
                    index_bean = Index(index_name=index,
                                       index_ticker=index_list[index],
                                       data=from_yahoo)
                    self.indexes.append(index_bean)

        except FileNotFoundError:
            print(f"file {file_conf} not found")
            exit(-1)
        except json.JSONDecodeError:
            print("Error in decoding json")
            exit(-1)
        except AttributeError:
            print("some attribute is None")
            exit(-1)

    def setup_daily_log_return(self):

        for index in self.indexes:
            index.daily_log_return = pd.DataFrame(index.df['Date'])
            index.daily_log_return['Daily Log Return'] = np.log(
                index.df['Adjusted Close'] / index.df['Adjusted Close'].shift(1)
            )
            index.daily_log_return.set_index('Date', inplace=True)
            index.daily_log_return.dropna()

    def setup_volatility(self, window=30):
        for index in self.indexes:
            dummy = pd.DataFrame(index.df[['Adjusted Close', 'Date']])
            dummy['Adjusted Close'].pct_change().dropna()
            dummy.set_index('Date', inplace=True)
            index.volatility = dummy['Adjusted Close'].rolling(window=window).std().dropna()

    def print_indexes(self):
        print(Loader.__LINES)
        print("Analyzing this index list: {")
        for index in self.indexes:
            print(f'\t{index}')
        print(f'}}\n{Loader.__LINES}')
