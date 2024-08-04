"""
Choong Min Um <choongmin.um@unh.edu>

This module helps to rebalance my portfolio according to the Zacks
Stock Screener result.
"""

import argparse
import datetime
import yfinance as yf
from pprint import pprint

# Enter user-specific information.
dir_downloads = '/mnt/c/Users/funda/Downloads/'
dir_results = '/home/cmu-linux/repos/stock-screening/screeningResults/'
account_no = '235427167'
position_core = 'SPAXX**'

# Read lines of a csv file.
def read_lines(file):
    infile = open(dir_downloads+f'{file}', 'r')
    lines = infile.readlines()
    infile.close()
    return lines


# Get new tickers from the Stock Screener.
def get_tickers_new(file_new):
    tickers_new = []
    lines = read_lines(file_new)
    for line in lines[1:]:
        tokens = line.split(',')
        tickers_new.append(tokens[1].replace('"', ''))
    return tickers_new


# Recommend which stocks to trade.
def recommend_trades(file_new, file_current, indicator_buffett):
    lines = read_lines(file_current)
    tickers_new = get_tickers_new(file_new)

    # Determine account total, amount per stock, and current tickers.
    account_total = 0
    tickers_current = []
    for line in lines:
        tokens = line.split(',')
        if line.startswith(account_no):
            if tokens[7] != '':
                account_total = account_total + float(tokens[7].strip('$'))
            if tokens[2] not in [position_core, 'Pending Activity']:
                tickers_current.append(tokens[2])
    per_stock = account_total / indicator_buffett / len(tickers_new)

    # Write the new tickers to a file.
    date_today = datetime.datetime.now().strftime('%y%m%d')
    outfile = open(dir_results + f'{date_today}.txt', 'w')
    outfile.write(
            f'Balance: ${account_total}\n'
            f'Buffett Indicator: {indicator_buffett}\n'
            '\n'
            '// Zacks //\n'
            'Supreme Valuation\t\tMorningstar\n'
            )
    for element in tickers_new:
        outfile.write(f'{element}\n')
    outfile.close()

    # Determine which tickers to sell, rebalance, and buy.
    tickers_sell = set(tickers_current) - (
            set(tickers_new) & set(tickers_current)
            )
    tickers_rebalance = set(tickers_new) & set(tickers_current)
    tickers_buy = set(tickers_new) - (set(tickers_new) & set(tickers_current))

    # Determine how to rebalance and buy stocks.
    dict_rebalance = {}
    dict_buy = {}
    for line in lines:
        tokens = line.split(',')
        if line.startswith(account_no):
            if tokens[2] in tickers_rebalance:
                dict_rebalance[tokens[2]] = round(
                        (per_stock - float(tokens[7].strip('$'))) 
                        / yf.Ticker(tokens[2]).info['currentPrice']
                        )
    for element in tickers_buy:
        dict_buy[element] = round(
                per_stock / yf.Ticker(element).info['currentPrice']
                )
    trade_stocks = {
            'Account Total': f'${account_total}',
            'Stocks': sorted(tickers_new),
            'Number of Stocks': len(tickers_new),
            'Amount Per Stock': f'${round(per_stock, 2)}',
            'Sell': sorted(tickers_sell),
            'Rebalance': dict_rebalance,
            'Buy': dict_buy
            }

    return trade_stocks


def get_args():
    parser = argparse.ArgumentParser(
            description=(
                'This module helps to rebalance my portfolio according to the '
                'Zacks Stock Screener result.'
                )
            )
    parser.add_argument('file_new', help='Zacks Stock Screener result file')
    parser.add_argument('file_current', help='current portfolio file')
    parser.add_argument(
            'indicator_buffett',
            type=float,
            help='Buffett Indicator'
            )
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    pprint(
            recommend_trades(
                args.file_new,
                args.file_current,
                args.indicator_buffett
                ),
            sort_dicts=False
            )


if __name__ == '__main__':
    main()
