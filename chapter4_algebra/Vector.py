# the simplest form-scratch approach is to represent vectors as lists of numbers
# one problem with this approach is that we will want to perform arithmetic on vectors
# to begin with, we'll frequently need to add two vectors.
# Vectors add componentwise.

def vector_add(v, w):
    """add corresponding elements"""
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def vector_substract(v, w):
    """substracts corresponding elements"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def vector_sum(vectors):
    """sums all corresponding elements"""
    result = vectors[0]
    for vector in vectors[1:]:
        result = vector_add(result, vector)
        return result


def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]


def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1 / n, vector_sum(vectors))


def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)


import math


def magnitude(v):
    return math.sqrt(sum_of_squares(v))


def squared_distance(v, w):
    """(v_1 * w_1) ** 2 + ... + (v_n * w_n) ** 2"""
    return sum_of_squares(vector_substract(v, w))


def distance(v, w):
    return math.sqrt(squared_distance(v, w))


def distance2(v, w):
    return magnitude(vector_substract(v, w))

# Using lists as vectors is great for exposition but terrible for performance
# In production code, you would want to use the NumPy library.
