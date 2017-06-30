import math
from matplotlib import pyplot as plt
import random


def normal_cdf(x, mu=0, sigma=1):  # cumulative distribution function
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


def normal_pdf(x, mu=0, sigma=1):
    coefficient = 1 / (math.sqrt(2 * math.pi) * sigma)
    return coefficient * math.exp(-(x - mu) ** 2 / 2 / sigma ** 2)


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


# we have a coin and we want to test whether it's fair
# assumption: the coin has some probability p of landing heads
# null hypothesis: the coin is fair, that is, that p = 0.5

# our test involves flipping the coin some number n times
# and counting the number of heads X
# Each coin flip is a Bernoulli trial, which means that X is a Binomial(n,p) random variable
# which we can approximate using the normal distribution

def normal_approximation_to_binomial(n, p):
    """finds mu and sigma corresponding to Binomial(n,p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


# Whenever a random variable follows a normal distribution, we can use normal_cdf
# to figure out the probability that is realized value lies within (or outside) a particular interval



# the normal cdf is the probability the variable is below a threshold
normal_propability_below = normal_cdf


# it's above the threshold if it is not below the threshold
def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)


# it's between if it's less than hi, but not less than lo
def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


# it's outside if it's not between
def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)


def normal_upper_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z<=z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z >= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability, mu=0, sigma=1):  # ???
    """returns the symmectric (about the mean) bounds that contain the specified probability"""
    tail_probability = (1 - probability) / 2
    # upper bound should have tail propability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)
    # lower bound should have tail probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)
    return lower_bound, upper_bound


mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)  # flip the coin 1000 times and p = 0.5
print("mu_0:", mu_0, "sigma_0:", sigma_0)
significance = normal_two_sided_bounds(0.95, mu_0, sigma_0)  # willingness set at 5%
print("significance:", significance)

# the power of a test, which is tha probability of not making a type 2 error,
# in which we fail to reject H0 even thought it's false
# knowing merely tha p is not 0.5 doesn't give you a ton of information about the
# distribution of X
# let's check what happens if p is really 0.55



# 95% bounds based on assumption p is 0.5
lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

# actual mu and sigma based on p = 0.55
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
print("mu_1:", mu_1, "sigma_1:", sigma_1)

# a type 2 error means we fail to reject the null hypothesis
# which will happen when X is still in our original interval
type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type_2_probability
print(power)

hi = normal_upper_bound(0.95, mu_0, sigma_0)
type_2_probability = normal_propability_below(hi, mu_1, sigma_1)
power = 1 - type_2_probability
print("power:", power)  # ???


def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, the tail is what's greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail is what's less than x
        return 2 * normal_propability_below(x, mu, sigma)


a = two_sided_p_value(529.5, mu_0, sigma_0)
print(a)

# extreme_value_count = 0
# for _ in range(100000):
#     nun_heads = sum(1 if random.random() < 0.5 else 0 for _ in range(1000))
#     if nun_heads >= 530 or nun_heads <= 470:
#         extreme_value_count += 1
# print(extreme_value_count)
# print((extreme_value_count / 100000))
#
# a=two_sided_p_value(531.5,mu_0,sigma_0)
# print(a)



# confidence interval
# we can estimate the probability of the unfair coin by looking at the average value
# of the Bernoulli variables corresponding to each flip—1 if heads, 0 if tails.
# If we observe 525 heads out of 1,000 flips, then we estimate p equals 0.525.
p_hat = 525 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)

a = normal_two_sided_bounds(0.95, mu, sigma)
print(a)  # we do not conclude that the coin is unfair, since 0.5 falls within
# our confidence interval

p_hat = 540 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)

a = normal_two_sided_bounds(0.95, mu, sigma)
print(a)


# p-hacking
def run_experiment():
    """flip a fair coin 1000 times, True = heads, False = tails"""
    return [random.random() < 0.5 for _ in range(1000)]


def reject_fairness(experiment):
    """using the 5% significance levels"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 468 or num_heads > 531


random.seed(0)
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment for experiment in experiments if reject_fairness(experiment)])


print(num_rejections)