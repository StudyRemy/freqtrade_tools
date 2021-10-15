# Coincompare

A script that compares the coins of a few different exchanges to see which coins are unique on an exchange (and thus an easier prey for pump & dump) to put in a blacklist.
After running this script several blacklist files in .json-format are generated for usage with the [Freqtrade](https://github.com/freqtrade/freqtrade) bot.  .


It compares between (and only between) Binance, KuCoin, Huobi, Okex and Coinbase. So most of the biggest exchanges are covered.  

The coin might be on another small exchange, but that won't be an issue, I think. If the coin gets pumped on one of the big ones the existence of the coin on a small exchange won't matter.