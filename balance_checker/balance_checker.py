# Checks the balance of Binance, Kucoin and Huobi

import ccxt
import config

# Create exchange-objects
binance = ccxt.binance ({
    'apiKey': config.BINANCE_API,
    'secret': config.BINANCE_SECRET
})

kucoin = ccxt.kucoin ({
    'apiKey': config.KUCOIN_API,
    'secret': config.KUCOIN_SECRET,
    'password': config.KUCOIN_PASSWORD
})

huobi = ccxt.huobipro ({
    'apiKey': config.HUOBI_API,
    'secret': config.HUOBI_SECRET
})

# Checks balance
def balance_checker(exchange):
    try:
        balance = exchange.fetch_balance()
        total_balance = 0

        for i in balance['total']:
            if balance['total'].get(i) > 0.0001:
                if i != 'USDT':
                    your_balance = balance['total'][i]
                    remaining_balance = your_balance
                    try:
                        orderbook = exchange.fetch_order_book(str(i) + '/USDT')
                    except:
                        try:
                            orderbook = exchange.fetch_order_book(str(i) + '/BUSD')
                        except:
                            try:
                                orderbook = exchange.fetch_order_book(str(i) + '/BTC')
                            except:
                                print('No ' + str(i) + ' pairs!')

                    cost = 0
                    for bid in orderbook['bids']:
                        if remaining_balance <= bid[1]:
                            cost += bid[0] * remaining_balance
                            break
                        else:
                            cost += bid[0] * bid[1]
                        remaining_balance = max(0, remaining_balance - bid[1])
    
                else:
                    cost = balance['total'].get(i)
                total_balance += cost
        return total_balance            

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')

def check_balance_binance():
    return round(balance_checker(binance))

def check_balance_kucoin():
    return round(balance_checker(kucoin))

def check_balance_huobi():
    return round(balance_checker(huobi))

def check_balance_total():
    return check_balance_binance() + check_balance_kucoin() + check_balance_huobi()

def check_BTC_value():
    return round(binance.fetch_order_book('BTC/USDT')['bids'][0][0])