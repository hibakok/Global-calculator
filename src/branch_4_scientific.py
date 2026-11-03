# Ветвь 4. Научные функции.
# Открывает научный блок калькулятора: модуль, знак, корень,
# экспоненту, логарифм, тригонометрию и константы pi, e.

from branch_1_arithmetic import add, divide


def abs_value(x):
    """Возвращает модуль числа x: abs_value(-3) = 3."""
    if x < 0:
        return -x
    return x


def sign(x):
    """Возвращает знак числа x: -1, 0 или 1."""
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def sqrt_real(x):
    """Возвращает вещественный квадратный корень из неотрицательного числа x."""
    if x < 0:
        raise ValueError("Корень из отрицательного числа не определён.")
    if x == 0:
        return 0
    y = divide(add(x, 1), 2)
    while True:
        nxt = divide(add(y, divide(x, y)), 2)
        if not (nxt < y):
            return y
        y = nxt
