import random


def random_kid():
    return random.choice(["boy", "girl"])


both_girls = 0
older_girl = 0
either_girl = 0

random.seed(0)
for _ in range(100000):
    younger = random_kid()
    older = random_kid()
    if older == "girl":
        older_girl += 1
    if older == "girl" and younger == "girl":
        both_girls += 1
    if older == "girl" or younger == "girl":
        either_girl += 1
print(older_girl, both_girls, either_girl)
print("P(both | older): ", both_girls / older_girl)
print("P(both | either): ", both_girls / either_girl)


def uniform_pdf(x):
    return 1 if 0 <= x < 1 else 0


# Python's random.random() is a [pseudo]random variable with a uniform density

def uniform_cdf(x):
    """returns the propability that a uniform random variable is <= x"""
    if x < 0:
        return 0
    elif x < 1:
        return x
    else:
        return 1


import math


def normal_pdf(x, mu=0, sigma=1):
    coefficient = 1 / (math.sqrt(2 * math.pi) * sigma)
    return coefficient * math.exp(-(x - mu) ** 2 / 2 / sigma ** 2)


from matplotlib import pyplot as plt

xs = [x / 10.0 for x in range(-50, 50)]
plt.plot(xs, [normal_pdf(x, sigma=1) for x in xs], "-", label="mu=0,sigma=1")
plt.plot(xs, [normal_pdf(x, sigma=2) for x in xs], "--", label="mu=0,sigma=2")
plt.plot(xs, [normal_pdf(x, sigma=0.5) for x in xs], ":", label="mu=0,sigma=0.5")
plt.plot(xs, [normal_pdf(x, mu=-1) for x in xs], "-.", label="mu=-1,sigma=1")
plt.legend()
plt.title("Various Normal pdfs")
plt.show()


def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


xs = [x / 10.0 for x in range(-50, 50)]
plt.plot(xs, [normal_cdf(x, sigma=1) for x in xs], '-', label='mu=0,sigma=1')
plt.plot(xs, [normal_cdf(x, sigma=2) for x in xs], '--', label='mu=0,sigma=2')
plt.plot(xs, [normal_cdf(x, sigma=0.5) for x in xs], ':', label='mu=0,sigma=0.5')
plt.plot(xs, [normal_cdf(x, mu=-1) for x in xs], '-.', label='mu=-1,sigma=1')
plt.legend(loc=4)  # bottom right
plt.title("Various Normal cdfs")
plt.show()


# to compute inverse with
# normal_cdf is continuous and strictly increasing
# with binary search

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):  ### wonderful
    """find approximate inverse using binary search"""
    # if not standard, compute standard and rescal
    if mu != 0 or sigma != 1:  ###
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = -10.0, 0  # normal_cdf(-10) is very close to 0
    hi_z, hi_p = 10.0, 1  # normal_cdf(10) is very close to 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2
        mid_p = normal_pdf(mid_z)
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still to high, search below it
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z


# the mean is p, the standard deviation is math.sqrt(p*(1-p))
def bernoulli_trial(p):
    return 1 if random.random() < p else 0


# according to the central limit theorem
# mean u=np
# standard deviation sigma=math.sqrt(np(1-p))
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))


from collections import Counter


def make_hist(p, n, num_points):
    data = [binomial(n, p) for _ in range(num_points)]

    # user a bar chart to show the actual binominal samples
    histogram = Counter(data)
    plt.bar([x for x in histogram.keys()],
            [v / num_points for v in histogram.values()],  # v /num_points = probability
            0.8, color='0.75')

    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))

    # use a line chart to show the normal approximation
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu, sigma) for i in xs]
    plt.plot(xs,ys)
    plt.title("Binomial Distribution vs. Normal Approximation")
    plt.show()

make_hist(0.75,100,10000)