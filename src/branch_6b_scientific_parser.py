# Ветвь 6b. Научные выражения: таблицы имён, операции и парсер.
# Даёт смысл именам из Ветви 6a: константы pi и e, функции sqrt,
# exp, ln, sin, cos, tan. Вещественная степень "^" через
# power_real Ветви 4. Главная функция — calculate_scientific.

from branch_1_arithmetic import subtract
from branch_3b_parser import apply_binary, current_token
from branch_4_scientific import (
    sqrt_real, exp_real, get_e, ln_positive, power_real,
)
from branch_5_trigonometry import get_pi, sin_rad, cos_rad, tan_rad
from branch_6a_scientific_tokenizer import tokenize_scientific


def apply_scientific(op, a, b):
    """Применяет бинарную операцию op к числам a и b; "^" возводит в вещественную степень."""
    if op == "^":
        return power_real(a, b)
    return apply_binary(op, a, b)


def is_constant(name):
    """Возвращает True, если имя name — имя известной константы: pi или e."""
    return name == "pi" or name == "e"


def constant_value(name):
    """Возвращает значение константы по имени: pi или e."""
    if name == "pi":
        return get_pi()
    if name == "e":
        return get_e()
    raise ValueError("Неизвестная константа: '" + name + "'.")


def is_function(name):
    """Возвращает True, если имя name — имя известной функции: sqrt, exp, ln, sin, cos, tan."""
    return name in ("sqrt", "exp", "ln", "sin", "cos", "tan")


def apply_function(name, x):
    """Применяет функцию по имени name к числу x."""
    if name == "sqrt":
        return sqrt_real(x)
    if name == "exp":
        return exp_real(x)
    if name == "ln":
        return ln_positive(x)
    if name == "sin":
        return sin_rad(x)
    if name == "cos":
        return cos_rad(x)
    if name == "tan":
        return tan_rad(x)
    raise ValueError("Неизвестная функция: '" + name + "'.")


def parse_call(tokens, pos):
    """Разбирает вызов функции: имя, скобка, аргумент-выражение, скобка; возвращает пару (значение, позиция)."""
    name = current_token(tokens, pos)[1]
    if current_token(tokens, pos + 1)[0] != "left_paren":
        raise ValueError("После имени функции '" + name + "' ожидалась открывающая скобка.")
    inner, next_pos = parse_expression_scientific(tokens, pos + 2)
    if current_token(tokens, next_pos)[0] != "right_paren":
        raise ValueError("Ожидалась закрывающая скобка после аргумента функции '" + name + "'.")
    return apply_function(name, inner), next_pos + 1


def parse_factor_scientific(tokens, pos):
    """Разбирает множитель научного выражения: число, константу, вызов функции, скобку или унарный знак; возвращает пару (значение, позиция)."""
    kind, value = current_token(tokens, pos)
    if kind == "number":
        return value, pos + 1
    if kind == "name":
        if is_function(value):
            return parse_call(tokens, pos)
        if is_constant(value):
            return constant_value(value), pos + 1
        raise ValueError("Неизвестное имя: '" + value + "'.")
    if kind == "operator" and value == "-":
        inner, next_pos = parse_power_scientific(tokens, pos + 1)
        return subtract(0, inner), next_pos
    if kind == "operator" and value == "+":
        return parse_power_scientific(tokens, pos + 1)
    if kind == "left_paren":
        result, next_pos = parse_expression_scientific(tokens, pos + 1)
        if current_token(tokens, next_pos)[0] != "right_paren":
            raise ValueError("Ожидалась закрывающая скобка.")
        return result, next_pos + 1
    raise ValueError("Ожидалось число, имя, открывающая скобка или унарный знак.")


def parse_power_scientific(tokens, pos):
    """Разбирает возведение в вещественную степень (правоассоциативно); возвращает пару (значение, позиция)."""
    base, pos = parse_factor_scientific(tokens, pos)
    kind, op = current_token(tokens, pos)
    if kind == "operator" and op == "^":
        exponent, next_pos = parse_power_scientific(tokens, pos + 1)
        return apply_scientific(op, base, exponent), next_pos
    return base, pos


def parse_term_scientific(tokens, pos):
    """Разбирает цепочку умножения, деления и остатка; возвращает пару (значение, позиция)."""
    value, pos = parse_power_scientific(tokens, pos)
    while True:
        kind, op = current_token(tokens, pos)
        if kind != "operator" or op not in "*/%":
            return value, pos
        right, pos = parse_power_scientific(tokens, pos + 1)
        value = apply_scientific(op, value, right)


def parse_expression_scientific(tokens, pos):
    """Разбирает цепочку сложения и вычитания; возвращает пару (значение, позиция)."""
    value, pos = parse_term_scientific(tokens, pos)
    while True:
        kind, op = current_token(tokens, pos)
        if kind != "operator" or op not in "+-":
            return value, pos
        right, pos = parse_term_scientific(tokens, pos + 1)
        value = apply_scientific(op, value, right)


def calculate_scientific(s):
    """Вычисляет научное выражение из строки s и возвращает число."""
    tokens = tokenize_scientific(s)
    if not tokens:
        raise ValueError("Пустое выражение.")
    value, pos = parse_expression_scientific(tokens, 0)
    if pos != len(tokens):
        raise ValueError("Выражение разобрано не до конца.")
    return value