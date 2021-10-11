# Is this file necessary at all? Either expand on it or move it to telegrammer

import pandas
import datetime

def calculate_percent(value, exchange):
    df = pandas.read_csv('crypto_info.csv', index_col = 0)

    if exchange == 'binance':
        starter_value = (df['Binance'].astype(float))[0]
    if exchange == 'kucoin':
        starter_value = df['Kucoin'].astype(float)[0]
    if exchange == 'huobi':
        starter_value = df['Huobi'].astype(float)[0]
    if exchange == 'total':
        starter_value = df['Total'].astype(float)[0]
    
    return round((value/starter_value - 1)*100, 2)

def get_value(exchange, date):
    df = pandas.read_csv('crypto_info.csv', index_col = 0)

    if exchange == 'binance':
        binance_df = (df['Binance'].astype(float))
        binance_day_df = binance_df.loc[date]
        value = binance_day_df.iloc[0]
    if exchange == 'kucoin':
        kucoin_df = (df['Kucoin'].astype(float))
        kucoin_day_df = kucoin_df.loc[date]
        value = kucoin_day_df.iloc[0]
    if exchange == 'huobi':
        huobi_df = (df['Huobi'].astype(float))
        huobi_day_df = huobi_df.loc[date]
        value = huobi_day_df.iloc[0]
    if exchange == 'total':
        total_df = (df['Total'].astype(float))
        total_day_df = total_df.loc[date]
        value = total_day_df.iloc[0]
    if exchange == 'BTC':
        total_df = (df['BTC value'].astype(float))
        total_day_df = total_df.loc[date]
        value = total_day_df.iloc[0]

    return round(value)


def calculate_BTC_diff(value):
    df = pandas.read_csv('crypto_info.csv', index_col = 0)
    starter_value = df['BTC value'].astype(float)[0]
    return round((value/starter_value - 1)*100, 2)

#today = datetime.date.today().strftime("%Y-%m-%d")

#print(get_value('binance', today))
