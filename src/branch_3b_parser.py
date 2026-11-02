# Ветвь 3b. Разбор выражений: парсер и вычислитель.
# Собирается из методов Ветвей 1, 2 и 3a.

from branch_1_arithmetic import add, subtract, multiply, divide
from branch_2_extended import remainder, power_int
from branch_3a_tokenizer import tokenize, make_token


def current_token(tokens, pos):
    """Возвращает токен на позиции pos или токен ("end", None) за концом списка."""
    if pos < len(tokens):
        return tokens[pos]
    return make_token("end", None)


def power_signed(a, n):
    """Возводит число a в целую степень n, в том числе отрицательную."""
    if not isinstance(n, int):
        raise ValueError("Степень должна быть целым числом.")
    if n >= 0:
        return power_int(a, n)
    return divide(1, power_int(a, subtract(0, n)))


def apply_binary(op, a, b):
    """Применяет бинарную операцию op к числам a и b."""
    if op == "+":
        return add(a, b)
    if op == "-":
        return subtract(a, b)
    if op == "*":
        return multiply(a, b)
    if op == "/":
        return divide(a, b)
    if op == "%":
        return remainder(a, b)
    if op == "^":
        return power_signed(a, b)
    raise ValueError("Неизвестная операция: '" + str(op) + "'.")


def parse_factor(tokens, pos):
    """Разбирает множитель: число, скобку или унарный знак; возвращает (значение, позиция)."""
    kind, value = current_token(tokens, pos)
    if kind == "number":
        return value, pos + 1
    if kind == "operator" and value == "-":
        inner, next_pos = parse_power(tokens, pos + 1)
        return subtract(0, inner), next_pos
    if kind == "operator" and value == "+":
        return parse_power(tokens, pos + 1)
    if kind == "left_paren":
        result, next_pos = parse_expression(tokens, pos + 1)
        if current_token(tokens, next_pos)[0] != "right_paren":
            raise ValueError("Ожидалась закрывающая скобка.")
        return result, next_pos + 1
    raise ValueError("Ожидалось число, открывающая скобка или унарный знак.")


def parse_power(tokens, pos):
    """Разбирает возведение в степень (правоассоциативно); возвращает (значение, позиция)."""
    base, pos = parse_factor(tokens, pos)
    kind, op = current_token(tokens, pos)
    if kind == "operator" and op == "^":
        exponent, next_pos = parse_power(tokens, pos + 1)
        return apply_binary(op, base, exponent), next_pos
    return base, pos


def parse_term(tokens, pos):
    """Разбирает цепочку умножения, деления и остатка; возвращает (значение, позиция)."""
    value, pos = parse_power(tokens, pos)
    while True:
        kind, op = current_token(tokens, pos)
        if kind != "operator" or op not in "*/%":
            return value, pos
        right, pos = parse_power(tokens, pos + 1)
        value = apply_binary(op, value, right)


def parse_expression(tokens, pos):
    """Разбирает цепочку сложения и вычитания; возвращает (значение, позиция)."""
    value, pos = parse_term(tokens, pos)
    while True:
        kind, op = current_token(tokens, pos)
        if kind != "operator" or op not in "+-":
            return value, pos
        right, pos = parse_term(tokens, pos + 1)
        value = apply_binary(op, value, right)


def calculate(s):
    """Вычисляет арифметическое выражение из строки s и возвращает число."""
    tokens = tokenize(s)
    if not tokens:
        raise ValueError("Пустое выражение.")
    value, pos = parse_expression(tokens, 0)
    if pos != len(tokens):
        raise ValueError("Выражение разобрано не до конца.")
    return value
