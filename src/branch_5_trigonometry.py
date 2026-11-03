# Ветвь 5. Тригонометрия.
# Число пи по формуле Мэчина, приведение угла, синус, косинус
# и тангенс собственными рядами Тейлора. Собирается из методов
# Ветвей 1 и 4 (abs_value).

from branch_1_arithmetic import add, subtract, multiply, divide
from branch_4_scientific import abs_value


def arctan_series(z):
    """Суммирует ряд Тейлора арктангенса z - z^3/3 + z^5/5 - ... для |z| < 1."""
    if z <= -1 or z >= 1:
        raise ValueError("Ряд арктангенса определён для -1 < z < 1.")
    zz = multiply(z, z)
    term = z
    total = z
    k = 1
    while True:
        term = multiply(multiply(term, zz), subtract(multiply(2, k), 1))
        term = subtract(0, divide(term, add(multiply(2, k), 1)))
        total = add(total, term)
        if not (abs_value(term) > multiply(abs_value(total), 1e-16)):
            return total
        k = add(k, 1)


def get_pi():
    """Возвращает число пи по формуле Мэчина: 16*arctan(1/5) - 4*arctan(1/239)."""
    return subtract(multiply(16, arctan_series(0.2)),
                    multiply(4, arctan_series(divide(1, 239))))


def reduce_angle(x):
    """Приводит угол x в радианах к паре (k, r), где x = k*pi + r и |r| <= pi/2."""
    if x != x:
        return 0, x
    if x == float("inf") or x == float("-inf"):
        raise ValueError("Тригонометрия бесконечного угла не определена.")
    k = round(divide(x, get_pi()))
    r = subtract(x, multiply(k, get_pi()))
    return k, r


def sin_series(r):
    """Суммирует ряд Тейлора синуса r - r^3/3! + r^5/5! - ... для |r| <= pi/2."""
    term = r
    total = r
    k = 1
    while True:
        term = multiply(multiply(term, r), r)
        term = subtract(0, divide(term, multiply(multiply(2, k), add(multiply(2, k), 1))))
        total = add(total, term)
        if not (abs_value(term) > multiply(abs_value(total), 1e-16)):
            return total
        k = add(k, 1)


def cos_series(r):
    """Суммирует ряд Тейлора косинуса 1 - r^2/2! + r^4/4! - ... для |r| <= pi/2."""
    term = 1.0
    total = 1.0
    k = 1
    while True:
        term = multiply(multiply(term, r), r)
        term = subtract(0, divide(term, multiply(multiply(2, k), subtract(multiply(2, k), 1))))
        total = add(total, term)
        if not (abs_value(term) > multiply(abs_value(total), 1e-16)):
            return total
        k = add(k, 1)


def sin_rad(x):
    """Возвращает синус угла x, заданного в радианах."""
    k, r = reduce_angle(x)
    result = sin_series(r)
    if k % 2 == 1:
        result = subtract(0, result)
    return result


def cos_rad(x):
    """Возвращает косинус угла x, заданного в радианах."""
    k, r = reduce_angle(x)
    result = cos_series(r)
    if k % 2 == 1:
        result = subtract(0, result)
    return result


def tan_rad(x):
    """Возвращает тангенс угла x, заданного в радианах."""
    return divide(sin_rad(x), cos_rad(x))