# Ветвь 3a. Разбор выражений: токенизатор.
# Токен — пара (тип, значение). Типы: "number", "operator",
# "left_paren", "right_paren", "end".


def is_digit(c):
    """Возвращает True, если символ c — десятичная цифра."""
    return c in "0123456789"


def is_space(c):
    """Возвращает True, если символ c — пробельный."""
    return c in " \t\n\r"


def is_operator(c):
    """Возвращает True, если символ c — знак операции: + - * / % ^."""
    return c in "+-*/%^"


def skip_spaces(s, i):
    """Возвращает индекс первого непробельного символа строки s, начиная с позиции i."""
    while i < len(s) and is_space(s[i]):
        i += 1
    return i


def read_digits(s, i):
    """Возвращает позицию, идущую за последовательностью цифр, начатой в позиции i."""
    while i < len(s) and is_digit(s[i]):
        i += 1
    return i


def read_number(s, i):
    """Читает число из строки s с позиции i; возвращает пару (число, следующая позиция)."""
    end = read_digits(s, i)
    has_fraction = (end < len(s) and s[end] == "."
                    and end + 1 < len(s) and is_digit(s[end + 1]))
    if has_fraction:
        end = read_digits(s, end + 1)
        return float(s[i:end]), end
    return int(s[i:end]), end


def make_token(kind, value):
    """Возвращает токен — пару (тип, значение)."""
    return (kind, value)


def read_token(s, i):
    """Читает один токен из строки s с позиции i; возвращает пару (токен, следующая позиция)."""
    c = s[i]
    if is_digit(c):
        value, next_i = read_number(s, i)
        return make_token("number", value), next_i
    if is_operator(c):
        return make_token("operator", c), i + 1
    if c == "(":
        return make_token("left_paren", c), i + 1
    if c == ")":
        return make_token("right_paren", c), i + 1
    raise ValueError("Недопустимый символ в выражении: '" + c + "'.")


def tokenize(s):
    """Разбирает строку выражения в список токенов; пробелы игнорируются."""
    tokens = []
    i = skip_spaces(s, 0)
    while i < len(s):
        token, i = read_token(s, i)
        tokens.append(token)
        i = skip_spaces(s, i)
    return tokens
