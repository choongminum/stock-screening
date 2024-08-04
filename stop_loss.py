"""
Choong Min Um <choongmin.um@unh.edu>

This module calculates the 10% stop-loss price per stock.
"""

import argparse
import yfinance as yf
from pprint import pprint

from rebalance import read_lines

# Enter user-specific information.
account_no = '235427167'
position_core = 'SPAXX**'


# Calculate the 10% stop-loss price per stock.
def get_stop_loss(file):
    lines = read_lines(file)

    # Determine current tickers.
    tickers_current = []
    for line in lines:
        tokens = line.split(',')
        if line.startswith(account_no):
            if tokens[2] not in [position_core, 'Pending Activity']:
                tickers_current.append(tokens[2])

    # Create a dictionary with the stop-loss price per stock.
    dict_stop_loss = {}
    for element in tickers_current:
        price_stop_loss = round(
                0.9 * yf.Ticker(element).info['currentPrice'],
                2
                )
        dict_stop_loss[element] = f'${price_stop_loss}'

    return dict_stop_loss


def get_args():
    parser = argparse.ArgumentParser(
            description=(
                'This module calculates the 10% stop-loss price per stock.'
                )
            )
    parser.add_argument('file', help='current portfolio file')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    pprint(get_stop_loss(args.file))


if __name__ == '__main__':
    main()
