import csv
from datetime import datetime

from dateutil.relativedelta import relativedelta

with open('api/data.csv') as file:
    csv_reader = csv.DictReader(file, delimiter=',')
    data = [row for row in csv_reader]
data.sort(key=lambda i: datetime.strptime(i['Timestamp'], '%Y-%m-%d'))

attrs = list(data[0].keys())
attrs.remove('Id')
attrs.remove('Timestamp')

values = [list(set(row[attr] for row in data)) for attr in attrs]


def date_range(start_date, end_date, grouping):
    time = start_date
    if grouping == 'monthly':
        while time < end_date:
            yield time - relativedelta(months=1), time
            time += relativedelta(months=1)
        yield time - relativedelta(months=1), end_date
    elif grouping == 'daily':
        while time < end_date:
            yield time
            time += relativedelta(days=1)
        yield time
    else:
        step = (1, 2)[('weekly', 'bi-weekly').index(grouping)]
        while time < end_date:
            yield time - relativedelta(weeks=step), time
            time += relativedelta(weeks=step)
        yield time - relativedelta(weeks=step), end_date


def filter_by_filters(data_item, filters):
    for data_filter in filters:
        if data_item[data_filter] != filters[data_filter]:
            return False
    return True


def get_value_by_period(start_date, end_date, sample_type, old_value, filters):
    dates_for_this_period = [date.strftime('%Y-%m-%d') for date in date_range(start_date, end_date, 'daily') if
                             start_date < date <= end_date]
    datas_for_this_period = []
    data_in_period = False
    for data_item in data:
        if data_item['Timestamp'] in dates_for_this_period:
            datas_for_this_period.append(data_item)
            data_in_period = True
        elif data_in_period:
            break
    value = len(tuple(i for i in datas_for_this_period if filter_by_filters(i, filters)))
    return value if sample_type == 'usual' else value + old_value
