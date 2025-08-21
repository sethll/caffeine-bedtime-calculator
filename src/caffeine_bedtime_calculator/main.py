"""
Calculator to determine bedtime based on caffeine consumption amount and time.

Copyright (C) 2025  Seth L

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import click
import datetime as dt
from operator import itemgetter
import math

from . import __version__

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

ONE_HALF = float(0.5)
CAFFEINE_LAMBDA = float(5.7)


def split_time_amount(time_amount):
    """Parse time:amount string and return datetime and caffeine amount.

    Args:
        time_amount (str): Format 'HHMM:amount' where HHMM is 24-hour time
                          and amount is caffeine in milligrams.

    Returns:
        tuple: (datetime object for today at specified time, float amount)

    Example:
        >>> split_time_amount('1430:200')
        (datetime(2025, 8, 17, 14, 30), 200.0)
    """
    caf_time, amount = time_amount.split(":")
    my_today = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d")
    caf_time = my_today + caf_time
    caf_time = dt.datetime.strptime(caf_time, "%Y%m%d%H%M")

    amount = float(amount)

    return caf_time, amount


def calc_total_time_in_hours(passed_time):
    """Convert a timedelta to total hours as float.

    Args:
        passed_time (timedelta): Time difference to convert

    Returns:
        float: Total time in hours

    Example:
        >>> calc_total_time_in_hours(timedelta(hours=2, minutes=30))
        2.5
    """
    [hours, minutes, seconds] = str(passed_time).split(":")
    days_and_hours = hours.split(" ")

    if len(days_and_hours) > 1:
        hours = days_and_hours[-1]
        days = days_and_hours[0]
        hours = float(days) * 24 + float(hours)

    total_time = float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    total_time = total_time / 3600

    return total_time


def calculate_X(x_origin, passed_time):
    """Calculate remaining caffeine using exponential decay formula.

    Uses the formula: X = Xo * (1/2)^(T/5.7)
    where 5.7 hours is the half-life of caffeine.

    Args:
        x_origin (float): Initial caffeine amount in milligrams
        passed_time (timedelta): Time elapsed since consumption

    Returns:
        float: Remaining caffeine amount in milligrams
    """
    got_x = float()
    t_time = calc_total_time_in_hours(passed_time)
    got_x = x_origin * ONE_HALF ** (t_time / CAFFEINE_LAMBDA)

    return got_x


def calculate_T(x_origin, target_caf_mg):
    """Calculate time needed to reach target caffeine level.

    Uses the formula: T = 5.7 * (ln(Ca/Xo)/ln(1/2))
    where Ca is target amount and Xo is current amount.

    Args:
        x_origin (float): Current caffeine amount in milligrams
        target_caf_mg (float): Target caffeine amount in milligrams

    Returns:
        float: Time in hours to reach target level
    """
    t_value = CAFFEINE_LAMBDA * (
        math.log(target_caf_mg / x_origin) / math.log(ONE_HALF)
    )

    return t_value


@click.command()
@click.argument("target", type=int)
@click.argument("time_amount", nargs=-1, required=True)
@click.version_option(version=__version__, prog_name="cbc")
def main(target, time_amount):
    """\b
    Caffeine Bedtime Calculator. 2025, Seth L
    Version: 0.1.0

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
        cbc 75 '1100:300' '1500:5'
    """
    all_inputs = list()

    for user_input in time_amount:
        time_amount_tuple = split_time_amount(user_input)
        all_inputs.append(time_amount_tuple)

    all_inputs.sort(key=itemgetter(0))
    first_item = all_inputs.pop(0)
    previous_time_marker = first_item[0]
    running_caffeine = first_item[1]

    for each in all_inputs:
        passed_time = each[0] - previous_time_marker
        running_caffeine = calculate_X(running_caffeine, passed_time)
        running_caffeine += each[1]
        previous_time_marker = each[0]

    the_time_now = dt.datetime.now()
    passed_time = the_time_now - previous_time_marker
    running_caffeine = calculate_X(running_caffeine, passed_time)

    print("Caffeine remaining in system: {}mg".format(round(running_caffeine, 2)))

    t_value = calculate_T(running_caffeine, float(target))
    bedtime = the_time_now + dt.timedelta(hours=t_value)

    print(
        "Reach target for sleep ({}mg) at: {}".format(
            target, dt.datetime.strftime(bedtime, "%Y-%m-%d %H:%M")
        )
    )


if __name__ == "__main__":
    main()
