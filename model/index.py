import pandas as pd


class Index:

    def __init__(self, index_name: str, index_ticker: str, data: pd.DataFrame):
        self.i_name = index_name
        self.i_ticker = index_ticker
        self.df = data
        self.daily_log_return = None
        self.volatility = None


    def __str__(self):
        return f'{{name: {self.i_name}, ticker: {self.i_ticker}, data_size:{self.df.size}}}'

    def __repr__(self):
        return self.__str__()

