import quandl
import pandas as pd



def generate_dataset():
    '''
    Queries Quandl for information
    '''

    bitcoin = pd.DataFrame(quandl.get('BCHARTS/BITSTAMPUSD')['Close'])
    bitcoin.rename(columns={'Close':'BTC'}, inplace=True)
    
    print bitcoin.head()
    #djia = pd.DataFrame(quandl.get('GOOG/INDEXDJX_DJI')['Close'])
    #djia.rename(columns={'Close': 'DJIA'}, inplace=True)
    
    #df = pd.merge(bitcoin, djia, how='inner', left_index=True,
    #              right_index=True)

    #print df

if __name__ == '__main__':
    generate_dataset()

