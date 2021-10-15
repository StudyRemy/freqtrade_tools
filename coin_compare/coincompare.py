import sys
import ccxt

# Gets the available coins on the exchange
def getmarkets(exchange):
    markets = exchange.load_markets()
    items = []
    for item in markets:
        if '/' in item:
            quote = item.split("/")[0]
        elif '-' in item:
            quote = item.split("-")[0]
        if quote not in items:
            items.append(quote)
    return items

# compare the coins between the exchange and other exchanges
def uniqueinexchange(exchange, other1, other2, other3, other4):
    list =[]
    for item in exchange:
        if item not in other1 and item not in other2 and item not in other3 and item not in other4:
            list.append(item)
    return list

# creates text for a ready to use blacklist.json
def createstring(inputlist, currency=None):
    string = "{\n    \"exchange:\"\n        \"pair_blacklist\": [\n"
    if currency is None:
        string += "\"("
        for ind, item in enumerate(inputlist):
            if item is inputlist[-1]:
                string += item + ")/.*\""
            elif ind!=0 and ind%10==0:
                string += item + ")/.*\",\n\"("
            else:
                string += item + "|"
        return string
    for item in inputlist:
        if item is not inputlist[-1]:
            string += "        \"" + item + "/"+ currency + "\", \n"
        if item is inputlist[-1]:
            string += "        \"" + item + "/"+ currency + "\"\n"
    string += "    ]\n}"
    return string

# prints the list to a file
def printtofile(unique, exchange):
    original_stdout = sys.stdout
    filename = "" + exchange + "-blacklist.json"
    with open(filename, 'w') as f:
        sys.stdout = f
        print(unique)
        sys.stdout = original_stdout

binance = ccxt.binance()
kucoin = ccxt.kucoin()
huobi = ccxt.huobipro()
okex = ccxt.okex()
coinbasepro = ccxt.coinbasepro()

kucoinmarkets = getmarkets(kucoin)
binancemarkets = getmarkets(binance)
huobimarkets = getmarkets(huobi)
okexmarkets = getmarkets(okex)
coinbasepromarkets = getmarkets(coinbasepro)

uniqueinkucoin = uniqueinexchange(kucoinmarkets, binancemarkets, huobimarkets, okexmarkets, coinbasepromarkets)
uniqueinbinance = uniqueinexchange(binancemarkets, kucoinmarkets, huobimarkets, okexmarkets, coinbasepromarkets)
uniqueinhuobi = uniqueinexchange(huobimarkets, kucoinmarkets, binancemarkets, okexmarkets, coinbasepromarkets)
uniqueinokex = uniqueinexchange(okexmarkets, huobimarkets, kucoinmarkets, binancemarkets, coinbasepromarkets)
uniqueincoinbase = uniqueinexchange(coinbasepromarkets, huobimarkets, kucoinmarkets, binancemarkets, okexmarkets)

# Edit or out-comment this to your liking
printtofile(createstring(uniqueinkucoin, "USDT"), 'KuCoin')
printtofile(createstring(uniqueinhuobi, "USDT"), 'Huobi')
printtofile(createstring(uniqueinokex, "USDT"), 'Okex')
printtofile(createstring(uniqueincoinbase, "USDT"), 'Coinbase')
printtofile(createstring(uniqueinbinance, "USDT"), 'BinanceUSDT')
printtofile(createstring(uniqueinbinance, "BUSD"), 'BinanceBUSD')
printtofile(createstring(uniqueinbinance, "BTC"), 'BinanceBTC')