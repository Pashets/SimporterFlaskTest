from datetime import datetime

from flask import request, Blueprint

from .utils import date_range, get_value_by_period, attrs, values

api = Blueprint('api', __name__)


@api.route('/info')
def info():
    return dict(status='success', attrs=attrs, values=values)


@api.route('/timeline')
def timeline_route():
    params = request.args
    if not {'startDate', 'endDate', 'Type', 'Grouping'}.issubset(set(params.keys())):
        return dict(status='error', message='Not all params are present!')
    start_date, end_date, sample_type, grouping = params['startDate'], params['endDate'], params['Type'], params[
        'Grouping']
    filters = {param: params[param] for param in params if param in attrs}
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return dict(status='error', message='startDate is invalid!')
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return dict(status='error', message='endDate is invalid!')
    if sample_type not in ('cumulative', 'usual'):
        return dict(status='error', message='Type is invalid!')
    if grouping not in ('weekly', 'bi-weekly', 'monthly'):
        return dict(status='error', message='Grouping is invalid!')

    timeline = []
    value = 0
    for start_period, end_period in date_range(start_date, end_date, grouping):
        value = get_value_by_period(start_period, end_period, sample_type, value, filters)
        timeline.append(dict(date=end_period.strftime('%Y-%m-%d'), value=value))
    return dict(status='success', timeline=timeline)
