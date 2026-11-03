# Ветвь 6a. Научные выражения: токенизатор.
# Расширяет токенизатор Ветви 3a: имена-«name» (sqrt, pi, sin)
# и числа с показателем степени (1e3, 2.5e-4). Ветвь 6a не
# знает ни констант, ни функций — она только делит строку на
# токены; смысл именам даст Ветвь 6b.

from branch_3a_tokenizer import (
    is_digit, read_digits, read_number, read_token, skip_spaces,
    make_token,
)


def is_letter(c):
    """Возвращает True, если символ c — латинская буква."""
    return c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def read_name(s, i):
    """Возвращает позицию, идущую за последовательностью латинских букв, начатой в позиции i."""
    while i < len(s) and is_letter(s[i]):
        i += 1
    return i


def is_exponent_letter(c):
    """Возвращает True, если символ c — буква показателя степени: e или E."""
    return c == "e" or c == "E"


def has_exponent(s, j):
    """Возвращает True, если в позиции j начинается показатель степени: e/E с цифрой или со знаком и цифрой."""
    if j >= len(s) or not is_exponent_letter(s[j]):
        return False
    if j + 1 < len(s) and is_digit(s[j + 1]):
        return True
    return (j + 2 < len(s) and (s[j + 1] == "+" or s[j + 1] == "-")
            and is_digit(s[j + 2]))


def exponent_digits_start(s, j):
    """Возвращает позицию первой цифры показателя степени, начатого буквой e/E в позиции j."""
    if s[j + 1] == "+" or s[j + 1] == "-":
        return j + 2
    return j + 1


def read_number_exp(s, i):
    """Читает число с показателем степени (1e3, 2.5e-4) из строки s с позиции i; возвращает пару (число, следующая позиция)."""
    value, end = read_number(s, i)
    if not has_exponent(s, end):
        return value, end
    end = read_digits(s, exponent_digits_start(s, end))
    return float(s[i:end]), end


def read_token_scientific(s, i):
    """Читает один токен научного выражения из строки s с позиции i; возвращает пару (токен, следующая позиция)."""
    c = s[i]
    if is_digit(c):
        value, next_i = read_number_exp(s, i)
        return make_token("number", value), next_i
    if is_letter(c):
        end = read_name(s, i)
        return make_token("name", s[i:end]), end
    return read_token(s, i)


def tokenize_with(s, read_one):
    """Разбирает строку s в список токенов читателем read_one; пробелы игнорируются."""
    tokens = []
    i = skip_spaces(s, 0)
    while i < len(s):
        token, i = read_one(s, i)
        tokens.append(token)
        i = skip_spaces(s, i)
    return tokens


def tokenize_scientific(s):
    """Разбирает строку научного выражения в список токенов; пробелы игнорируются."""
    return tokenize_with(s, read_token_scientific)