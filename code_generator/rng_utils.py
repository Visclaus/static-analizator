from random import randint as rng


# возвращает рандомный элемент указанного множества
def r_v(params):
    return params[rng(0, len(params) - 1)]


# генерирует n неповторяющихся значений от min до max
def gen_n_rands(n, min_v, max_v):
    rands = []
    if n == 0:
        return rands
    for index in range(n):
        cur_rng = rng(min_v, max_v)
        while cur_rng in rands:
            cur_rng = rng(min_v, max_v)
        rands.append(cur_rng)
    return rands
