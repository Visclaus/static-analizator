from random import randint as rng


# возвращает рандомный элемент указанного множества
def rand_value(params):
    return params[rng(0, len(params) - 1)]


# генерирует n неповторяющихся значений от min до max
def gen_n_rands(n, min_v, max_v):
    rands = []
    if n == 0:
        return rands
    if n >= max_v - min_v + 1:
        raise Exception("value of 'n' parameter is too big for given [min_v, max_v]")
    for index in range(n):
        cur_rng = rng(min_v, max_v)
        while cur_rng in rands:
            cur_rng = rng(min_v, max_v)
        rands.append(cur_rng)
    return rands
