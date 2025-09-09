"""
Choong Min Um <choongmin.um@unh.edu>

This module calculates the 10% stop-loss price per stock.
"""

import argparse
import yfinance as yf
from pprint import pprint
from rebalance import read_lines

# Enter user-specific information.
account_no = {"Z05672323": "Stock Trading", "235427167": "Rollover IRA"}
position_core = ["FZFXX**", "SPAXX**"]


# Calculate the 10% stop-loss price per stock.
def get_stop_loss(file):
    lines = read_lines(file)

    # Create a dictionary with the stop-loss price per stock.
    dict_stop_loss = {}
    for line in lines:
        tokens = line.split(",")
        if tokens[0] in account_no.keys():
            if tokens[2] not in [
                *position_core,
                "Pending Activity",
                "Pending activity",
            ]:
                price = 0.9 * float(tokens[14].strip("$"))
                dict_stop_loss[f"{tokens[2]}"] = f"${price:.2f}"
    return dict_stop_loss


def get_args():
    parser = argparse.ArgumentParser(
        description=(
            "This module calculates the 10% stop-loss price per stock."
        )
    )
    parser.add_argument("file", help="current portfolio file")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    pprint(get_stop_loss(args.file))


if __name__ == "__main__":
    main()
