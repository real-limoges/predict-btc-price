import quandl
import pandas as pd

API_KEY = open(API_KEY).read().strip()

BITCOIN = 'BCHARTS/BITSTAMPUSD'
CLOSE = 'Close'
RATE = 'Rate'
US_10_YR = '10 YR'

SOURCES = { 'GOOG/INDEXDJX_DJI': 'DJIA',
            'USTREASURY/YIELD': 'US_10_YR',
            'YAHOO/INDEX_RUT': 'RUS2000',
            'YAHOO/INDEX_SSEC': 'SSEC',
            'CURRFX/USDEUR' : 'EURO',
            'CURRFX/USDJPY' : 'YEN',
            'CURRFX/USDCHF' : 'SWISS'}


def generate_dataset():
    '''
    Queries Quandl for information
    '''

    df  = pd.DataFrame(quandl.get(BITCOIN, api_key=API_KEY)[CLOSE]).rename(
                       columns={CLOSE: 'BTC'})

    for k,v  in SOURCES.iteritems():
        new_data = quandl.get(k, api_key = API_KEY)
        
        if '10 YR' in new_data.columns:
            new_data = pd.DataFrame(new_data[US_10_YR]).rename(
                                    columns={US_10_YR: v})
        elif 'Close' in new_data.columns:
            new_data = pd.DataFrame(new_data[CLOSE]).rename(
                columns={CLOSE: v})

        elif 'Rate' in new_data.columns:
            new_data = pd.DataFrame(new_data[RATE]).rename(
                columns={RATE: v})

        #Merges the new_data column onto the dataset
        df = pd.merge(df, new_data, how='left', left_index=True,
                      right_index=True)
    
    return df


def interpolate(df, method='time'):
    '''
    Interpolates the data
    '''

    for col in df.columns:
        df[col] = df[col].interpolate(method=method)

    return df
    
if __name__ == '__main__':
    df = interpolate( generate_dataset() ).to_csv('../data/dataset.csv')
    
