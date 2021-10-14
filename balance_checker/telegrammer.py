from telegram import *
from telegram.ext import *
import balance_checker as checker
import config
import stats
import datetime
from dateutil.relativedelta import relativedelta

FIRST_DAY = stats.get_first_day()

def calc_values(exchange, date):
    exchange_obj = checker.check_exchange(exchange)

    value = checker.balance_checker(exchange_obj)
    value_old = stats.get_value(exchange, date)
    percent = round((value/value_old - 1)*100, 2)

    return value, value_old, percent

def get_balance_total(update: Update, context: CallbackContext) -> None:
    value_BN, value_BN_old, percent_BN = calc_values('binance', FIRST_DAY)
    value_KC, value_KC_old, percent_KC = calc_values('kucoin', FIRST_DAY)
    value_HB, value_HB_old, percent_HB = calc_values('huobi', FIRST_DAY)

    value = value_BN + value_KC + value_HB
    value_old = value_BN_old + value_KC_old + value_HB_old
    percent = round((value/value_old - 1)*100, 2)

    BTC_perc = stats.calculate_BTC_diff(checker.check_BTC_value())
    diff = round(percent - BTC_perc, 2)
    update.message.reply_text(f'<pre>Your total portfolio is worth ${round(value)}, this is a net profit of ${round(value - value_old)}\nThe difference since ' + FIRST_DAY + f' is {"{:.2f}".format(percent)}% \nBTC has changed {"{:.2f}".format(BTC_perc)}% \nThe difference between portfolio change and market change is {diff}%</pre>', parse_mode=ParseMode.HTML)

def create_message(date):
    value_BN, value_BN_old, percent_BN = calc_values('binance', date)
    value_KC, value_KC_old, percent_KC = calc_values('kucoin', date)
    value_HB, value_HB_old, percent_HB = calc_values('huobi', date)

    value_tot = value_BN + value_KC + value_HB
    value_tot_old = value_BN_old + value_KC_old + value_HB_old
    percent_tot = round((value_tot/value_tot_old - 1)*100, 2)
    value_btc = checker.check_BTC_value()
    value_btc_old = stats.get_value('BTC', date)
    percent_btc = round((value_btc/value_btc_old - 1)*100, 2)
    diff = percent_tot - percent_btc

    msg = (f'<pre>======================================= \n'\
f'Exchange | ' + date + ' | now   | % diff  \n'\
'---------+------------+-------+-------- \n'\
f'Binance  | ${value_BN_old}      | ${round(value_BN)} | {"{:.2f}".format(percent_BN)}%   \n'\
f'Kucoin   | ${value_KC_old}       | ${round(value_KC)}  | {"{:.2f}".format(percent_KC)}%   \n'\
f'Huobi    | ${value_HB_old}       | ${round(value_HB)}  | {"{:.2f}".format(percent_HB)}%   \n'\
'---------+------------+-------+-------- \n'\
f'Total    | ${value_tot_old}      | ${round(value_tot)} | {"{:.2f}".format(percent_tot)}%   \n'\
'---------+------------+-------+-------- \n'\
f'BTC      | ${value_btc_old}     | ${"{:.0f}".format(value_btc)}| {percent_btc}%   \n'\
'======================================= \n\n'\
f'Net profit is ${round(value_tot-value_tot_old)} \n'\
f'Difference between bots and market is {"{:.2f}".format(diff)}% </pre>')
    
    return msg

def get_balance_exchange(update: Update, context: CallbackContext) -> None:
    exchange = context.args[0]
    value, value_old, percent = calc_values(exchange, FIRST_DAY)
    update.message.reply_text(f'<pre>Your total ' + exchange + f' portfolio is worth ${round(value)}\nThe difference since ' + FIRST_DAY + f' is {percent}%</pre>', parse_mode=ParseMode.HTML)

def get_balance_alltime(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(create_message(FIRST_DAY), parse_mode=ParseMode.HTML)

def get_balance_daily(update: Update, context: CallbackContext) -> None:
    today = datetime.date.today().strftime("%Y-%m-%d")
    update.message.reply_text(create_message(today), parse_mode=ParseMode.HTML)

def get_balance_days(update: Update, context: CallbackContext) -> None:
    date = (datetime.date.today() - datetime.timedelta(days=int(context.args[0]))).strftime("%Y-%m-%d")
    update.message.reply_text(create_message(earliest_date(date)), parse_mode=ParseMode.HTML)

def get_balance_weekly(update: Update, context: CallbackContext) -> None:
    last_week = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    update.message.reply_text(create_message(earliest_date(last_week)), parse_mode=ParseMode.HTML)

def get_balance_monthly(update: Update, context: CallbackContext) -> None:
    last_month = (datetime.date.today() + relativedelta(months=-1)).strftime("%Y-%m-%d")

    update.message.reply_text(create_message(earliest_date(last_month)), parse_mode=ParseMode.HTML)

def earliest_date(date):
    if (FIRST_DAY > date):
        return FIRST_DAY
    else:
        return date

def start_telegram_bot():
    print("running Telegram crypto bot")
    updater = Updater(config.TOKEN)

    updater.dispatcher.add_handler(CommandHandler('exchange', get_balance_exchange))
    updater.dispatcher.add_handler(CommandHandler('total', get_balance_total))
    updater.dispatcher.add_handler(CommandHandler('alltime', get_balance_alltime))
    updater.dispatcher.add_handler(CommandHandler('daily', get_balance_daily))
    updater.dispatcher.add_handler(CommandHandler('days', get_balance_days))
    updater.dispatcher.add_handler(CommandHandler('weekly', get_balance_weekly))
    updater.dispatcher.add_handler(CommandHandler('monthly', get_balance_monthly))

    updater.start_polling()
    updater.idle()

start_telegram_bot()