# Ветвь 2. Расширенная арифметика.

from branch_1_arithmetic import add, subtract, multiply, divide

def power_int(a, n):
    """Возводит число a в целую неотрицательную степень n."""
    if n < 0:
        raise ValueError("Степень должна быть целой и неотрицательной.")
    result = 1
    for _ in range(n):
        result = multiply(result, a)
    return result


def int_divide(a, b):
    """Возвращает целую часть частного a / b, округлённую вниз."""
    if b == 0:
        raise ZeroDivisionError("Деление на ноль запрещено.")
    return a // b
    
def remainder(a, b):
    """Возвращает остаток от деления a на b (со знаком делителя)."""
    if b == 0:
        raise ZeroDivisionError("Деление на ноль запрещено.")
    return a % b

def percent(x, p):
    """Возвращает p процентов от числа x."""
    return divide(multiply(x, p), 100)
    
def root_int(x, n):
    """Возвращает целую часть корня степени n из неотрицательного целого x."""
    if not isinstance(x, int) or not isinstance(n, int):
        raise TypeError("root_int принимает только целые числа.")
    if n < 1:
        raise ValueError("Степень корня должна быть не меньше 1.")
    if x < 0:
        raise ValueError("Подкоренное число должно быть неотрицательным.")
    low = 0
    # Верхняя граница поиска: 2^ceil(биты(x) / n); её n-я степень всегда больше x.
    high = 1 << ((x.bit_length() + n - 1) // n)
    while subtract(high, low) > 1:
        mid = int_divide(add(low, high), 2)
        if power_int(mid, n) <= x:
            low = mid
        else:
            high = mid
    return low
