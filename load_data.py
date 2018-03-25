"""
    handle preprocessing and loading of data.
"""

import html
import os.path
import pandas as pd
import re

class LoadData:

    @classmethod
    def preprocess_stocktwits_data(cls, symbol):
        """
            preprocess the data and saves it as a csv file (stocktwits_'symbol'_preprocessed.csv)
            preprocesses in following ways:
            1) extract message and datetime columns.
            2) sort according to datetime in descending order (newest first)
            3) remove links, @ references, extra whitespaces
            4) decode html entities
        """

        dataFrame = pd.read_csv('data-extractor/stocktwits_'+symbol+'.csv', usecols=['datetime', 'message'], parse_dates=['datetime'], infer_datetime_format=True)
        dataFrame.sort_values(by='datetime', ascending=False)
        dataFrame['message'] = dataFrame['message'].apply(lambda x: re.sub('(www\.|https?://).*?(\s|$)|@.*?(\s|$)|\s+', ' ', x))
        dataFrame['message'] = dataFrame['message'].apply(lambda x: re.sub('^\s*|\s*$', '', x))
        dataFrame['message'] = dataFrame['message'].apply(lambda x: html.unescape(x))

        dataFrame.to_csv('data-extractor/stocktwits_'+symbol+'_preprocessed.csv', index=False)

    @classmethod
    def get_stocktwits_data(cls, symbol):
        """
            get_data loads the preprocessed data of 'symbol' from data-extractor
            and returns a pandas dataframe with columns [message(object), datetime(datetime64[ns])].
        """

        file_location = 'data-extractor/stocktwits_'+symbol+'_preprocessed.csv'
        if os.path.isfile(file_location) is False:
            LoadData.preprocess_stocktwits_data(symbol)

        dataFrame = pd.read_csv(file_location)
        return dataFrame