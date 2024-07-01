import os.path

import pandas as pd
import argparse
import logging

import os

logger = logging.getLogger(__name__)

def calculate_cost(usage:pd.DataFrame, tariffs:pd.DataFrame, economy='Economy 5'):
    usage['timestamp_day'] = pd.to_datetime(usage['timestamp']).dt.time.astype(str)
    usage = (
        usage
        .merge(
            tariffs.loc[economy].reset_index(drop=True).rename(columns={'timestamp': 'timestamp_day'}),
            on='timestamp_day',
            how='left',
        )
    )
    usage['cost'] = usage['primaryValue'] * usage['unit_price']
    return usage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--economy', type=str, default='Economy 5')
    parser.add_argument('--loadcurve', type=str, default='../business-1-utility-electricity-loadcurve.csv')
    parser.add_argument('--output', type=str, default='../business-1-utility-gas-costs.csv')
    args = parser.parse_args()

    usage = pd.read_csv(args.loadcurve, )
    tariffs = pd.read_csv('../economy_electricity_tariffs.csv').set_index('economy_type')

    usage = calculate_cost(usage, tariffs, args.economy)
    usage.to_csv(args.output, index=False)
    logging.info(f'Costs saved to {os.path.abspath(args.output)}')


if __name__ == '__main__':
    main()