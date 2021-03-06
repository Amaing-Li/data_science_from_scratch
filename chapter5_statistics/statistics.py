import collections

num_friends = [100, 49, 41, 40, 25]

num_points = len(num_friends)
largest_value = max(num_friends)
smallest_value = min(num_friends)


def mean(x):
    return sum(x) / len(x)


mean(num_friends)


def median(v):
    """finds the 'middle-most value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2

    if n % 2 == 1:
        # if odd, return the middle value
        return sorted_v[midpoint]
    else:
        # if even, return the average of the middle values
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2


median(num_friends)


def quantile(x, p):
    """return the pth-percentile value in x """
    p_index = int(p * len(x))
    return sorted(x)[p_index]


quantile(num_friends, 0.1)


def mode(x):
    """returns a list, might be more than one mode"""
    counts = collections.Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]


mode(num_friends)


# dispersion
def data_range(x):
    return max(x) - min(x)


def de_mean(x):
    """translate x by substracting its mean (so te result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)  ##


def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)


variance(num_friends)

import math


def standard_deviation(x):  # to better understand the data because vairance has a unit of squared
    return math.sqrt(variance(x))


def interquantile_range(x, p1, p2):  # more robust
    return quantile(x, p1) - quantile(x, p2)


interquantile_range(num_friends, 0.75, 0.25)


def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)


daily_minutes = [1]
covariance(num_friends, daily_minutes)


def correlation(x,y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x,y) /stdev_x /stdev_y
    else:
        return 0 # if no variation, corelation is zero