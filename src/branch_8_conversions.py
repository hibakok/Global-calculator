# Ветвь 8. Преобразования.
# Часть 1 — системы счисления: перевод целых чисел между
# основаниями 2-36 в обе стороны. Цепочки кирпичиков:
# число -> значения цифр -> строка (to_base_string) и строка ->
# значения цифр -> число (from_base_string); главная функция
# convert_base соединяет обе цепочки. Собирается из методов
# Ветвей 1 (add, subtract, multiply) и 2 (int_divide, remainder);
# существующие ветви не изменяются.

from branch_1_arithmetic import add, subtract, multiply
from branch_2_extended import int_divide, remainder

# Все цифры систем счисления; значение цифры — позиция её символа.
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def digit_char(value):
    """Возвращает символ цифры со значением value от 0 до 35."""
    if value < 0 or value > 35:
        raise ValueError("Значение цифры должно быть от 0 до 35.")
    return DIGITS[value]


def digit_value(char):
    """Возвращает значение одиночного символа цифры: '0'-'9' -> 0-9, 'a'-'z' и 'A'-'Z' -> 10-35."""
    if len(char) != 1:
        raise ValueError("Ожидался одиночный символ цифры, получено: '" + char + "'.")
    pos = DIGITS.find(char.lower())
    if pos == -1:
        raise ValueError("Символ '" + char + "' не является цифрой.")
    return pos


def check_base(base):
    """Проверяет, что основание системы счисления — целое от 2 до 36; возвращает его же."""
    if not isinstance(base, int):
        raise TypeError("Основание системы счисления должно быть целым числом.")
    if base < 2 or base > 36:
        raise ValueError("Основание системы счисления должно быть от 2 до 36.")
    return base


def check_integer(n):
    """Проверяет, что n — целое число, и возвращает его же."""
    if not isinstance(n, int):
        raise TypeError("Ожидалось целое число.")
    return n


def is_base_digit(char, base):
    """Возвращает True, если одиночный символ — допустимая цифра системы счисления с основанием base от 2 до 36."""
    return len(char) == 1 and char.lower() in DIGITS[:base]


def check_base_digit(char, base):
    """Проверяет, что символ — допустимая цифра при основании base, и возвращает её значение."""
    if not is_base_digit(char, base):
        raise ValueError("Символ '" + char + "' не является цифрой системы с основанием " + str(base) + ".")
    return digit_value(char)


def to_base_values(n, base):
    """Возвращает значения цифр целого числа n >= 0 по основанию base: список от младшей цифры к старшей."""
    if n < 0:
        raise ValueError("Ожидалось неотрицательное число: знак обрабатывает to_base_string.")
    values = []
    while True:
        values.append(remainder(n, base))
        n = int_divide(n, base)
        if n == 0:
            return values


def values_to_string(values):
    """Превращает список значений цифр (от старшей к младшей) в строку цифр."""
    chars = []
    for value in values:
        chars.append(digit_char(value))
    return "".join(chars)


def to_base_positive(n, base):
    """Переводит целое число n >= 0 в строку цифр по основанию base от 2 до 36."""
    return values_to_string(list(reversed(to_base_values(n, base))))


def to_base_string(n, base):
    """Главная функция перевода в систему счисления: целое число n -> строка цифр по основанию base."""
    check_base(base)
    check_integer(n)
    if n < 0:
        return "-" + to_base_positive(subtract(0, n), base)
    return to_base_positive(n, base)


def split_sign(s):
    """Отделяет знак числа: возвращает пару (знак: -1 или 1, строка цифр без знака и крайних пробелов)."""
    if not isinstance(s, str):
        raise TypeError("Ожидалась строка с числом.")
    stripped = s.strip()
    if stripped == "":
        raise ValueError("Пустая строка не является числом.")
    if stripped[0] == "-":
        return -1, stripped[1:].strip()
    if stripped[0] == "+":
        return 1, stripped[1:].strip()
    return 1, stripped


def from_base_digits(digits, base):
    """Вычисляет значение строки цифр (от старшей к младшей) по основанию base — схема Горнера."""
    total = 0
    for char in digits:
        total = add(multiply(total, base), check_base_digit(char, base))
    return total


def from_base_string(s, base):
    """Главная функция перевода из системы счисления: строка цифр со знаком -> целое число."""
    check_base(base)
    sign, digits = split_sign(s)
    if digits == "":
        raise ValueError("В строке нет ни одной цифры.")
    value = from_base_digits(digits, base)
    if sign < 0:
        return subtract(0, value)
    return value


def convert_base(s, from_base, to_base):
    """Переводит запись целого числа из одной системы счисления в другую: строка -> строка."""
    return to_base_string(from_base_string(s, from_base), to_base)