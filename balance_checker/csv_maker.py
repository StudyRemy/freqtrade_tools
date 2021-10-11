import csv
import os, sys
import datetime
import balance_checker as checker

today = datetime.date.today()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
#location = '/home/admin/balance_checker/crypto_info.csv'

with open(os.path.join(sys.path[0], 'crypto_info.csv'), mode='a', newline='') as crypto_file:
    fieldnames = ['date', 'time', 'BTC value', 'Binance', 'Kucoin', 'Huobi', 'Total']
    writer = csv.DictWriter(crypto_file, fieldnames=fieldnames)

    # checks exchanges, comment a line if you don't use it
    binance = checker.check_balance_binance()
    kucoin = checker.check_balance_kucoin()
    huobi = checker.check_balance_huobi()
    total = binance + kucoin + huobi

    # Run once with line below to create headers (for use in Excel) or use pre-created csv file
    #writer.writeheader()
    writer.writerow({'date': today, 'time': current_time, 'BTC value': checker.check_BTC_value(), 'Binance': binance, 'Kucoin': kucoin, 'Huobi': huobi, 'Total': total})