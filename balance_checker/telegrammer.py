from telegram import *
from telegram.ext import *
import balance_checker as checker
import config
import stats
import datetime

# TODO: Create message-creation function. Remove hardcoded strings
# TODO: Make generic balance checker with exchange as a parameter
# TODO: Make generic balance function with command as parameter?

def get_balance_binance(update: Update, context: CallbackContext) -> None:
    value = checker.check_balance_binance()
    percent = stats.calculate_percent(value, 'binance')
    update.message.reply_text(f'Your Binance portfolio is worth ${value}\n The difference since 14-10-\'21 is {percent}%')

def get_balance_kucoin(update: Update, context: CallbackContext) -> None:
    value = checker.check_balance_kucoin()
    percent = stats.calculate_percent(value, 'kucoin')
    update.message.reply_text(f'Your Kucoin portfolio is worth ${value}\n The difference since 14-10-\'21 is {percent}%')

def get_balance_huobi(update: Update, context: CallbackContext) -> None:
    value = checker.check_balance_huobi()
    percent = stats.calculate_percent(value, 'huobi')
    update.message.reply_text(f'Your Huobi portfolio is worth ${value}\n The difference since 14-10-\'21 is {percent}%')

def get_balance_total(update: Update, context: CallbackContext) -> None:
    value_BN = checker.check_balance_binance()
    percent_BN = stats.calculate_percent(value_BN, 'binance')
    value_KC = checker.check_balance_kucoin()
    percent_KC = stats.calculate_percent(value_KC, 'kucoin')
    value_HB = checker.check_balance_huobi()
    percent_HB = stats.calculate_percent(value_HB, 'huobi')
    value_tot = value_BN + value_KC + value_HB
    percent_tot = stats.calculate_percent(value_tot, 'total')
    BTC_perc = stats.calculate_BTC_diff(checker.check_BTC_value())
    diff = round(percent_tot - BTC_perc, 2)
    update.message.reply_text(f'Your total portfolio is worth ${value_tot}\nThe difference since 14-10-\'21 is {percent_tot}% \nBTC has changed {BTC_perc}% \nThe difference between portfolio change and market change is {diff}%')

# TODO: Create message-cretion function. Remove hardcoded strings
def get_balance_alltime(update: Update, context: CallbackContext) -> None:
    value_BN = checker.check_balance_binance()
    value_BN_old = stats.get_value('binance', '2021-10-14')
    percent_BN = round((value_BN/value_BN_old - 1)*100, 2)
    value_KC = checker.check_balance_kucoin()
    value_KC_old = stats.get_value('kucoin', '2021-10-14')
    percent_KC = round((value_KC/value_KC_old - 1)*100, 2)
    value_HB = checker.check_balance_huobi()
    value_HB_old = stats.get_value('huobi', '2021-10-14')
    percent_HB = round((value_HB/value_HB_old - 1)*100, 2)
    value_tot = value_BN + value_KC + value_HB
    value_tot_old = stats.get_value('total', '2021-10-14')
    percent_tot = round((value_tot/value_tot_old - 1)*100, 2)
    value_btc = checker.check_BTC_value()
    value_btc_old = stats.get_value('BTC', '2021-10-14')
    percent_btc = round((value_btc/value_btc_old - 1)*100, 2)
    diff = percent_tot - percent_btc
    update.message.reply_text(f'<pre>==================================== \n\
Exchange| 10-14-\'21 |  now  | % diff  \n\
---------+---------+-------+-------- \n\
Binance | ${value_BN_old}    | ${value_BN}  | {"{:.2f}".format(percent_BN)}%   \n\
Kucoin  | ${value_KC_old}     | ${value_KC}   | {"{:.2f}".format(percent_KC)}%   \n\
Huobi   | ${value_HB_old}     | ${value_HB}   | {"{:.2f}".format(percent_HB)}%   \n\
---------+---------+-------+-------- \n\
Total   | ${value_tot_old}   | ${value_tot} | {"{:.2f}".format(percent_tot)}%   \n\
---------+---------+-------+-------- \n\
BTC     | ${value_btc_old}  | ${"{:.0f}".format(value_btc)}| {percent_btc}%   \n\
==================================== \n\n\
Difference between bots and market is {"{:.2f}".format(diff)}% </pre>', parse_mode=ParseMode.HTML)

def get_balance_today(update: Update, context: CallbackContext) -> None:
    today = datetime.date.today().strftime("%Y-%m-%d")

    value_BN = checker.check_balance_binance()
    value_BN_old = stats.get_value('binance', today)
    percent_BN = round((value_BN/value_BN_old - 1)*100, 2)
    value_KC = checker.check_balance_kucoin()
    value_KC_old = stats.get_value('kucoin', today)
    percent_KC = round((value_KC/value_KC_old - 1)*100, 2)
    value_HB = checker.check_balance_huobi()
    value_HB_old = stats.get_value('huobi', today)
    percent_HB = round((value_HB/value_HB_old - 1)*100, 2)
    value_tot = value_BN + value_KC + value_HB
    value_tot_old = stats.get_value('total', today)
    percent_tot = round((value_tot/value_tot_old - 1)*100, 2)
    value_btc = checker.check_BTC_value()
    value_btc_old = stats.get_value('BTC', today)
    percent_btc = round((value_btc/value_btc_old - 1)*100, 2)
    diff = percent_tot - percent_btc
    update.message.reply_text(f'<pre>==================================== \n\
Exchange| midnight | now   | % diff  \n\
---------+---------+-------+-------- \n\
Binance | ${value_BN_old}    | ${value_BN}  | {"{:.2f}".format(percent_BN)}%   \n\
Kucoin  | ${value_KC_old}     | ${value_KC}   | {"{:.2f}".format(percent_KC)}%   \n\
Huobi   | ${value_HB_old}     | ${value_HB}   | {"{:.2f}".format(percent_HB)}%   \n\
---------+---------+-------+-------- \n\
Total   | ${value_tot_old}   | ${value_tot} | {"{:.2f}".format(percent_tot)}%   \n\
---------+---------+-------+-------- \n\
BTC     | ${value_btc_old}  | ${"{:.0f}".format(value_btc)}| {percent_btc}%   \n\
==================================== \n\n\
Difference between bots and market is {"{:.2f}".format(diff)}% </pre>', parse_mode=ParseMode.HTML)

def start_telegram_bot():
    print("running Telegram crypto bot")
    updater = Updater(config.TOKEN)

    # TODO: Change commands
    updater.dispatcher.add_handler(CommandHandler('binance', get_balance_binance))
    updater.dispatcher.add_handler(CommandHandler('kucoin', get_balance_kucoin))
    updater.dispatcher.add_handler(CommandHandler('huobi', get_balance_huobi))
    updater.dispatcher.add_handler(CommandHandler('total', get_balance_total))
    updater.dispatcher.add_handler(CommandHandler('alltime', get_balance_alltime))
    updater.dispatcher.add_handler(CommandHandler('today', get_balance_today))

    updater.start_polling()
    updater.idle()

start_telegram_bot()