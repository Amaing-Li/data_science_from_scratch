def magic(*args, **kwargs):
    print("unnamed args:", args)
    print("keyword args:", kwargs)


magic(1, 2, key="word", key2="word2")


def other_way_magic(x, y, z):
    return x + y + z


x_y_list = [1, 2]
z_dict = {"z": 3}
print(other_way_magic(*x_y_list, **z_dict))


def double_correct(f):
    """works no matter what kind of inputs f expects"""

    def g(*args, **kwargs):
        """whatever arguments g is supplied, pass then though to f"""
        return 2 * f(*args, **kwargs)

    return g


def f2(x, y):
    return x + y


g = double_correct(f2)
print(g(1,2))