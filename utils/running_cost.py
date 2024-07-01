import os.path

import pandas as pd
import numpy as np
import argparse
import logging

import os

logger = logging.getLogger(__name__)


def half_hour_running_cost(usage:pd.DataFrame, tariffs:pd.DataFrame, economy:str='Economy 5'):
    usage['timestamp_day'] = pd.to_datetime(usage['timestamp']).dt.time.astype(str)
    usage = (
        usage
        .merge(
            tariffs.loc[economy]
            .reset_index(drop=True)
            .rename(columns={'timestamp': 'timestamp_day'}),
            on='timestamp_day',
            how='left',
        )
    )
    usage['cost'] = usage['primaryValue'] * usage['unit_price']
    return usage


def projected_yearly_cost_range(appliance:pd.Series, half_hour_cost:pd.DataFrame):
    upfront_cost = appliance['upfront_cost']
    running_cost = half_hour_cost['cost'].sum()
    maintenance_cost = np.array([float(x) for x in appliance['annual_maintenance_cost'].split("-")])

    lifespan = appliance['lifetime'].split("-")
    if len(lifespan) == 1:
        lifespan = np.array([int(lifespan[0]), int(lifespan[0])])
    else:
        lifespan = np.array([int(x) for x in lifespan])

    # if maintenance cost is a range, take the average
    if isinstance(maintenance_cost, np.ndarray):
        maintenance_cost = np.mean(maintenance_cost)

    lifetime_cost = upfront_cost + running_cost + maintenance_cost
    yearly_cost = lifetime_cost / lifespan[::-1]

    return yearly_cost


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--economy', type=str, default='Economy 5')
    parser.add_argument('--loadcurve', type=str, default='../business-1-utility-electricity-loadcurve.csv')
    parser.add_argument('--output', type=str, default='../business-1-utility-gas-costs.csv')
    parser.add_argument('--appliance_id', type=str, default='1')
    args = parser.parse_args()

    usage = pd.read_csv(args.loadcurve)
    tariffs = pd.read_csv('../economy_electricity_tariffs.csv').set_index('economy_type')

    usage = half_hour_running_cost(usage, tariffs, args.economy)
    usage.to_csv(args.output, index=False)

    appliances = pd.read_csv('../appliances.csv', )
    appliance = appliances.iloc[int(args.appliance_id)]
    yearly_cost_range = projected_yearly_cost_range(appliance, usage)

    print(appliance)
    print(f'Yearly cost range: {yearly_cost_range[0]:.2f}-{yearly_cost_range[1]:.2f}')


if __name__ == '__main__':
    main()
