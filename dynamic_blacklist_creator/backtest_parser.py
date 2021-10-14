# Parses latest freqtrade backtest and generates a string with pipe-seperated coins that generated a profit below a minimum profit

import json
import os, sys
import blacklist_create_config as config

# init variables
coins = []
coinstring = ''
min_profit = 0.008 # 0,8%
BT_directory = config.backtest_directory
BL_directory = config.blacklist_directory
temp_directory = config.temp_directory
# If in freqtrade directory
# BT_directory = sys.path[0]

# Get the name of the latest backtest
with open(os.path.join(BT_directory, '.last_result.json'), "r") as last_result_file:
    last_result = json.load(last_result_file)
    latest_backtest_file = last_result['latest_backtest']

# Open latest backtest

with open(os.path.join(BT_directory, latest_backtest_file), "r") as latest_backtest:
  data = json.load(latest_backtest)

strategies = data["strategy"]
for strategy_name in strategies:
    strategy = strategies[strategy_name]
    results_per_pair = strategy["results_per_pair"]
    for pair_result in results_per_pair:

        # get pairs with low profit than min_profit and put them in coins-list
        if pair_result["profit_mean"] < min_profit:
            pair = pair_result["key"]
            coin = pair.split("/", 1)
            coins.append(coin[0])
            currency = pair.split("/", 2)[1]

# write name of strategy to file for naming blacklist_file in blacklist creator
# If using strategy-list for backtest it only writes the last strategy
stratname_file = open(os.path.join(temp_directory, 'stratname.txt'), 'w')
stratname_file.write(str(strategy_name) + '\n' + str(currency))
        
 # sort coins, add delimiters and put them in a string
coins.sort()
for c in coins:
    coinstring += c + '|'

# write coin string to file
file_object = open(os.path.join(temp_directory, 'to_blacklist.txt'), 'a')
file_object.write(coinstring)

# close opened files
latest_backtest.close()
stratname_file.close()
file_object.close()