import json
import matplotlib.pyplot as plt
import numpy as np
from math import floor, trunc


def allan(data, tau):
    """
    Allan standard deviation
    @param data: list with data [x1,...xn]
    @param tau: list with counts of intervals
    @return: res: list [[allan, std, count], ...]
    """
    res = []
    for f in tau:
        k = 0
        int = []
        s = 0
        it = 0
        while k < len(data):
            se = data[k:k + f]

            if len(se) == f:
                int.append(np.mean(se))

                if it > 0:
                    s += (int[-1] - int[-2]) ** 2

            k += f
            it += 1

        if len(int) - 1 > 0:
            v = np.sqrt(1 / (2 * (len(int) - 1)) * s)
            err = v / np.sqrt(floor(len(data) / f))
            res.append([v, err, len(int) - 1])

    return res


def printDict(dict):
    """
    Just print dictionary in json format in form:
    {
    key_1 : value_1
    .
    .
    key_n : value_n
    }
    @param dict: python dictionary
    """
    print(json.dumps(dict, indent=5))


def roundList(l, index):
    """
    Round list for printing into text files

    @param l: line for rounding
    @param index: information for rounding, [[position1, number_of_decimal_places1],[position2, number_of_decimal_places2], ...]
    @return: l: rounded list
    """
    for j in index:
        a = '{:.' + str(j[1]) + 'f}'
        if l[j[0]] == '-':
            l[j[0]] = '-'
        else:
            l[j[0]] = a.format(l[j[0]])

    return l


def date_to_mjd(year, month, day):
    """
    :Author: Matt Davis
    :Website: http://github.com/jiffyclub

    Change to returning modified Julian date

    Convert a date to Julian Day.

    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet',
        4th ed., Duffet-Smith and Zwart, 2011.

    Parameters
    ----------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.

    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.

    day : float
        Day, may contain fractional part.

    Returns
    -------
    mjd : float
        modified Julian Day

    Examples
    --------
    Convert 6 a.m., February 17, 1985 to Julian Day

    >>> date_to_mjd(1985,2,17.25)
    2446113.75

    """
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month

    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
            (year == 1582 and month < 10) or
            (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = trunc(yearp / 100.)
        B = 2 - A + trunc(A / 4.)

    if yearp < 0:
        C = trunc((365.25 * yearp) - 0.75)
    else:
        C = trunc(365.25 * yearp)

    D = trunc(30.6001 * (monthp + 1))

    jd = B + C + D + day + 1720994.5

    return jd - 2400000.5


def rssq(x):
    """
    Root sum of squares

    @param x: numpy matrix m*n
    @return: res: root sum of squares by m lines
    """
    res = []

    for i in range(x.shape[0]):

        square_sum = 0
        for j in range(x.shape[1]):
            square_sum += x[i, j] * x[i, j]

        # print(np.sqrt(square_sum))
        res.append(np.sqrt(square_sum))

    return res


def movingAverage(x, n=50):
    """
    Return moving average with floating window

    @param x: list with data
    @param n: range for moving average (kernel), with n = 50 will be average from 101 values
    @return: res: moving averages
    @return: plot_range: range for plotting
    """
    res = []
    plot_range = []
    for i in range(n, len(x) - n):
        m = np.mean(x[i - n:i + n + 1])
        res.append(m)
        plot_range.append(i)

    return res, plot_range
