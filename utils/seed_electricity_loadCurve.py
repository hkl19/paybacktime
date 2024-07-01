#seed_electricity_loadCurve.py
import csv
import random
from datetime import datetime, timedelta

patterns = {
    'winter': {
        'weekday': [(0, 10.5, 'low'), (11, 13.5, 'high'), (14, 16.5, 'moderate'), (17, 21.5, 'high'), (22, 23.5, 'low')],
        'weekend': [(0, 10.5, 'low'), (11, 21.5, 'high'), (22, 23.5, 'low')],
    },
    'spring': {
        'weekday': [(0, 10.5, 'low'), (11, 13.5, 'high'), (14, 16.5, 'moderate'), (17, 21.5, 'high'), (22, 23.5, 'low')],
        'weekend': [(0, 10.5, 'low'), (11, 21.5, 'high'), (22, 23.5, 'low')],
    },
    'summer': {
        'weekday': [(0, 10.5, 'low'), (11, 13.5, 'high'), (14, 16.5, 'moderate'), (17, 21.5, 'high'), (22, 23.5, 'low')],
        'weekend': [(0, 10.5, 'low'), (11, 13.5, 'high'), (14, 16.5, 'moderate'), (17, 21.5, 'high'), (22, 23.5, 'low')],
    },
    'fall': {
        'weekday': [(0, 10.5, 'low'), (11, 13.5, 'high'), (14, 16.5, 'moderate'), (17, 21.5, 'high'), (22, 23.5, 'low')],
        'weekend': [(0, 10.5, 'low'), (11, 21.5, 'high'), (22, 23.5, 'low')],
    },
}

# Power consumption levels
levels = {
    'low': (3, 5),
    'moderate': (10, 15),
    'high': (25, 35),
}

def get_random_consumption(power_level):
    min_val, max_val = levels[power_level]
    return round(random.uniform(min_val, max_val), 1)

def get_season(date):
    month = date.month
    if 3 <= month < 6:
        return 'spring'
    elif 6 <= month < 9:
        return 'summer'
    elif 9 <= month < 12:
        return 'fall'
    else:
        return 'winter'

def add_days(date, days):
    return date + timedelta(days=days)

def is_before_or_equal_to(date1, date2):
    return date1 <= date2

def generate_consumption_data(device_id, mpxn, start_date, end_date, measurement_type, utility):
    consumption_data = []
    current_date = start_date

    while is_before_or_equal_to(current_date, end_date):
        season = get_season(current_date)
        is_weekday = current_date.weekday() < 5
        day_pattern = patterns[season]['weekday' if is_weekday else 'weekend']

        for start_hour, end_hour, power_level in day_pattern:
            start_time = current_date.replace(hour=int(start_hour), minute=int((start_hour % 1) * 60))
            end_time = current_date.replace(hour=int(end_hour), minute=int((end_hour % 1) * 60))

            while is_before_or_equal_to(start_time, end_time):
                consumption = get_random_consumption(power_level)
                consumption_data.append({
                    'business_id': device_id,
                    'mpxn': mpxn,
                    'timestamp': start_time,
                    'primaryValue': consumption,
                    'unit': 'kWh',
                    'measurementType': measurement_type,
                    'utility': utility,
                })
                start_time += timedelta(minutes=30)

        current_date = add_days(current_date, 1)

    return consumption_data

def main():
    business_id = 1
    mpxn = '9876543210'
    today = datetime.now()
    start_date = datetime(2023, 7, 1)
    end_date = today
    measurement_type = 'READ'
    utility = 'gas'

    consumption_data = generate_consumption_data(business_id, mpxn, start_date, end_date, measurement_type, utility)

    filename = f"business-{business_id}-utility-{utility}-loadcurve.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=consumption_data[0].keys())
        writer.writeheader()
        writer.writerows(consumption_data)

    print(f'Data saved to {filename}')


main()