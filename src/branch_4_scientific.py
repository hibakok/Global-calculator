# Ветвь 4. Научные функции: экспонента и логарифм.
# Открывает научный блок калькулятора: модуль, знак, корень,
# экспоненту, число e, натуральный логарифм и вещественную
# степень. Собирается из методов Ветвей 1 и 2.

from branch_1_arithmetic import add, subtract, multiply, divide
from branch_2_extended import power_int


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


def exp_series(x):
    """Суммирует ряд Тейлора экспоненты 1 + x + x^2/2! + ... для |x| <= 1."""
    term = 1.0
    total = 1.0
    n = 1
    while True:
        term = divide(multiply(term, x), n)
        total = add(total, term)
        if not (abs_value(term) > multiply(abs_value(total), 1e-16)):
            return total
        n = add(n, 1)


def exp_real(x):
    """Возвращает e в степени x — экспоненту любого вещественного числа."""
    y = float(x)
    if y == float("inf") or y == float("-inf"):
        return 0.0 if y == float("-inf") else y
    halves = 0
    while abs_value(y) > 1:
        y = divide(y, 2)
        halves = add(halves, 1)
    result = exp_series(y)
    for _ in range(halves):
        result = multiply(result, result)
    return result


def get_e():
    """Возвращает основание натурального логарифма — число e."""
    return exp_real(1)


def ln_series(u):
    """Суммирует ряд Тейлора логарифма u - u^2/2 + u^3/3 - ... для |u| <= 1/2."""
    if u <= -1 or u >= 1:
        raise ValueError("Ряд логарифма определён для -1 < u < 1.")
    term = u
    total = u
    k = 1
    while True:
        term = divide(multiply(multiply(term, u), k), add(k, 1))
        term = subtract(0, term)
        total = add(total, term)
        if not (abs_value(term) > multiply(abs_value(total), 1e-16)):
            return total
        k = add(k, 1)


def get_ln2():
    """Возвращает натуральный логарифм числа 2."""
    return multiply(2, ln_series(subtract(sqrt_real(2), 1)))


def ln_positive(x):
    """Возвращает натуральный логарифм положительного числа x."""
    if x <= 0:
        raise ValueError("Логарифм определён только для положительных чисел.")
    y = float(x)
    if y == float("inf"):
        return y
    twos = 0
    while y > 1.5:
        y = divide(y, 2)
        twos = add(twos, 1)
    while y < 0.75:
        y = multiply(y, 2)
        twos = subtract(twos, 1)
    return add(multiply(twos, get_ln2()), ln_series(subtract(y, 1)))


def power_real(a, b):
    """Возводит число a в вещественную степень b."""
    if isinstance(b, int) or (isinstance(b, float) and b.is_integer()):
        n = int(b)
        if n >= 0:
            return power_int(a, n)
        return divide(1, power_int(a, subtract(0, n)))
    if a != a or b != b:
        return float("nan")
    if a == 0:
        if b > 0:
            return 0.0
        raise ZeroDivisionError("Ноль нельзя возводить в отрицательную степень.")
    if a < 0:
        raise ValueError("Отрицательное основание допустимо только в целой степени.")
    return exp_real(multiply(b, ln_positive(a)))