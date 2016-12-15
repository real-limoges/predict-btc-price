'''
This module grabs data from Quandl.com using their REST API.
'''

import quandl
import pandas as pd

API_KEY = open('API_KEY.txt').read().strip()

BITCOIN = 'BCHARTS/BITSTAMPUSD'
CLOSE = 'Close'
RATE = 'Rate'
US_10_YR = '10 YR'

SOURCES = {'YAHOO/INDEX_DJI': 'DJIA',
           'USTREASURY/YIELD': 'US_10_YR',
           'YAHOO/INDEX_RUT': 'RUS2000',
           'YAHOO/INDEX_SSEC': 'SSEC',
           'CURRFX/USDEUR': 'EURO',
           'CURRFX/USDJPY': 'YEN',
           'CURRFX/USDCHF': 'SWISS'}


def generate_dataset():
    '''
    Queries Quandl for information
    '''

    bitcoin_data = pd.DataFrame(quandl.get(BITCOIN,
                                           api_key=API_KEY)[CLOSE]).rename(columns={CLOSE: 'BTC'})

    for source_k, source_v in SOURCES.iteritems():
        new_quandl = quandl.get(source_k, api_key=API_KEY)

        if '10 YR' in new_quandl.columns:
            new_quandl = pd.DataFrame(new_quandl[US_10_YR]).rename(
                columns={US_10_YR: source_v})
        elif 'Close' in new_quandl.columns:
            new_quandl = pd.DataFrame(new_quandl[CLOSE]).rename(
                columns={CLOSE: source_v})

        elif 'Rate' in new_quandl.columns:
            new_quandl = pd.DataFrame(new_quandl[RATE]).rename(
                columns={RATE: source_v})

        # Merges the new_quandl column onto the dataset
        bitcoin_data = pd.merge(
            bitcoin_data,
            new_quandl,
            how='left',
            left_index=True,
            right_index=True)

    return bitcoin_data


def interpolate(col, method='time'):
    '''
    Interpolates the data
    '''

    return col.interpolate(method=method)


if __name__ == '__main__':
    full_dataset = generate_dataset()

    for feature_col in full_dataset.columns:
        full_dataset[feature_col] = full_dataset[feature_col].interpolate(
                                                        method='time') 

    full_dataset.to_csv('../data/dataset.csv', index=False)
