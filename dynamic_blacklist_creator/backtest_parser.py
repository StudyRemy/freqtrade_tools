# Parses latest freqtrade backtest and generates a string with pipe-seperated coins that generated a profit below a minimum profit

import json
import os, sys

# Default this script is run inside the backtest directoy. Change if needed.

# init variables
coins = []
coinstring = ''
min_profit = 0.08

# Get the name of the latest backtest
with open(os.path.join(sys.path[0], '.last_result.json'), "r") as last_result_file:
    last_result = json.load(last_result_file)
    latest_backtest_file = last_result['latest_backtest']

# Open latest backtest

with open(os.path.join(sys.path[0], latest_backtest_file), "r") as latest_backtest:
  data = json.load(latest_backtest)

for x in data:
    if x == 'strategy':
        y = data[x]
        for z in y:
            q = y[z]
            for r in q:
                # Get results per pair
                if r == 'results_per_pair':
                    s = q[r]
                    for t in s:
                        # get pairs with low profit than min_profit and put them in coins-list
                        if t['profit_mean'] < min_profit:
                            string = t['key']
                            coin = string.split("/", 1)
                            coins.append(coin[0])

# sort coins, add delimiters and put them in a string
coins.sort()
for c in coins:
    coinstring += c + '|'
coinstring = coinstring[:-1]

# write coin string to file
file_object = open(os.path.join(sys.path[0], 'to_blacklist.txt'), 'a')
file_object.write(coinstring)

# close opened files
latest_backtest.close()
file_object.close()