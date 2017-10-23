#!/usr/bin/env python3.6

"""
Calculator to determine bedtime based on caffeine consumption amount and time.
"""

import click
import datetime as dt
from operator import itemgetter
import math

"""
Caffeine-in-body calculation

Caffeine-in-body, milligrams = X
Initial amount = Xo
time in hours since consumption = T

X = Xo * (1/2)^(T/5.7)
"""

"""
Time-to-certain-amount calculation
Ca = Certain amount

T = 5.7 * (ln(Ca/Xo)/ln(1/2))
"""


# CONSTANTS

VERSION = '0.0.2'
ONE_HALF = float(0.5)
CAFFEINE_λ = float(5.7)


def split_time_amount(time_amount):
    """Accept TTTT:AAA and split it up, perform calculations"""
    caf_time, amount = time_amount.split(':')
    my_today = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d')
    caf_time = my_today + caf_time
    caf_time = dt.datetime.strptime(caf_time, '%Y%m%d%H%M')

    amount = float(amount)

    return caf_time, amount


def calc_total_time_in_hours(passed_time):
    [hours, minutes, seconds] = str(passed_time).split(':')
    total_time = float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    total_time = total_time / 3600

    return total_time


def calculate_X(x_origin, passed_time):
    """Get X"""
    got_x = float()
    t_time = calc_total_time_in_hours(passed_time)
    got_x = x_origin * ONE_HALF**(t_time / CAFFEINE_λ)

    return got_x


def calculate_T(x_origin, target_caf_mg):
    """Get T"""
    t_value = CAFFEINE_λ * \
        (math.log(target_caf_mg / x_origin) / math.log(ONE_HALF))

    return t_value


@click.command()
@click.argument(
    'target',
    nargs=1
)
@click.argument(
    'time_amount',
    nargs=-1
)
def main(target, time_amount):
    """\b
    Caffeine Bedtime Calculator. 2017, Seth L
    Version: 0.0.2

    Calculates the date/time when you can reasonably expect your sleep to no
    longer be impaired by caffeine, based on a metabolic half-life of 5.7
    hours.

    \b
    TARGET:         Natural number. Target caffeine amount (in milligrams) for
                        bedtime. Recommendation: 50 to 100
    TIME_AMOUNT:    Format is '24-hour-time:Amount'. 'Amount' is milligrams of
                        caffeine. E.g, '1100:300'

    \b
    Example:
        python cbc.py 75 '1100:300' '1500:5'
    """
    all_inputs = list()

    for user_input in time_amount:
        time_amount_tuple = split_time_amount(user_input)
        all_inputs.append(time_amount_tuple)

    all_inputs.sort(key=itemgetter(0))
    first_item = all_inputs.pop(0)
    previous_time_marker = first_item[0]
    running_caffeine = first_item[1]
    # got_x = float()

    for each in all_inputs:
        passed_time = each[0] - previous_time_marker
        running_caffeine = calculate_X(running_caffeine, passed_time)
        running_caffeine += each[1]
        previous_time_marker = each[0]

    the_time_now = dt.datetime.now()
    passed_time = the_time_now - previous_time_marker
    running_caffeine = calculate_X(running_caffeine, passed_time)

    print("Caffeine remaining in system: {}mg".format(
        round(running_caffeine, 2))
    )

    t_value = calculate_T(running_caffeine, float(target))
    bedtime = the_time_now + dt.timedelta(hours=t_value)

    print("Reach target for sleep ({}mg) at: {}".format(
        target, dt.datetime.strftime(bedtime, '%Y-%m-%d %H:%M')))


if __name__ == '__main__':
    main()
