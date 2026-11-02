# Ветвь 1. Элементарная арифметика.


def add(a, b):
    """Возвращает сумму двух чисел: a + b."""
    return a + b
    
def subtract(a, b):
    """Возвращает разность двух чисел: a - b."""
    return a - b
    
def multiply(a, b):
    """Возвращает произведение двух чисел: a * b."""
    return a * b
    
def divide(a, b):
    """Возвращает частное двух чисел: a / b."""
    if b == 0:
        raise ZeroDivisionError("Деление на ноль запрещено.")
    return a / b
