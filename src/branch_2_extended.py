# Ветвь 2. Расширенная арифметика.

from branch_1_arithmetic import multiply


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
