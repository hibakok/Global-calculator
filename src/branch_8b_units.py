# Ветвь 8b. Преобразования: единицы измерения.
# Часть 2 ветви 8. Линейные категории (длина, масса, объём) переводятся
# через коэффициенты к базовой единице категории; температура переводится
# через промежуточные градусы Цельсия, потому что её шкалы сдвинуты.
# Собирается из методов Ветви 1 (add, subtract, multiply, divide);
# от части 1 ветви 8 (системы счисления) не зависит. Существующие
# ветви не изменяются.

from branch_1_arithmetic import add, subtract, multiply, divide

# Словари-константы: коэффициенты к базовой единице категории
# (длина — метр, масса — грамм, объём — литр). Создаются при загрузке
# модуля и никогда не изменяются — глобального изменяемого состояния
# нет (docs/conventions.txt, раздел 6). Чтобы добавить единицу в
# категорию, достаточно дописать элемент словаря и тесты к нему.
LENGTH_FACTORS = {"km": 1000.0, "m": 1.0, "dm": 0.1, "cm": 0.01, "mm": 0.001}
MASS_FACTORS = {"t": 1000000.0, "kg": 1000.0, "g": 1.0, "mg": 0.001}
VOLUME_FACTORS = {"kl": 1000.0, "l": 1.0, "ml": 0.001}
TEMPERATURE_UNITS = ("c", "f", "k")


def is_length_unit(name):
    """Возвращает True, если name — единица длины: km, m, dm, cm, mm."""
    return name in LENGTH_FACTORS


def length_factor(name):
    """Возвращает коэффициент единицы длины name к метрам; для неизвестной единицы — ValueError."""
    if not is_length_unit(name):
        raise ValueError("Неизвестная единица длины: '" + str(name) + "'.")
    return LENGTH_FACTORS[name]


def is_mass_unit(name):
    """Возвращает True, если name — единица массы: t, kg, g, mg."""
    return name in MASS_FACTORS


def mass_factor(name):
    """Возвращает коэффициент единицы массы name к граммам; для неизвестной единицы — ValueError."""
    if not is_mass_unit(name):
        raise ValueError("Неизвестная единица массы: '" + str(name) + "'.")
    return MASS_FACTORS[name]


def is_volume_unit(name):
    """Возвращает True, если name — единица объёма: kl, l, ml."""
    return name in VOLUME_FACTORS


def volume_factor(name):
    """Возвращает коэффициент единицы объёма name к литрам; для неизвестной единицы — ValueError."""
    if not is_volume_unit(name):
        raise ValueError("Неизвестная единица объёма: '" + str(name) + "'.")
    return VOLUME_FACTORS[name]


def linear_convert(x, from_factor, to_factor):
    """Переводит число x между линейными единицами: домножает на отношение коэффициентов."""
    return divide(multiply(x, from_factor), to_factor)


def convert_length(x, from_unit, to_unit):
    """Переводит длину x из единицы from_unit в единицу to_unit: convert_length(2, "km", "m") = 2000.0."""
    return linear_convert(x, length_factor(from_unit), length_factor(to_unit))


def convert_mass(x, from_unit, to_unit):
    """Переводит массу x из единицы from_unit в единицу to_unit: convert_mass(1, "t", "kg") = 1000.0."""
    return linear_convert(x, mass_factor(from_unit), mass_factor(to_unit))


def convert_volume(x, from_unit, to_unit):
    """Переводит объём x из единицы from_unit в единицу to_unit: convert_volume(1, "l", "ml") = 1000.0."""
    return linear_convert(x, volume_factor(from_unit), volume_factor(to_unit))


def celsius_to_kelvin(c):
    """Переводит температуру из градусов Цельсия в кельвины."""
    return add(c, 273.15)


def kelvin_to_celsius(k):
    """Переводит температуру из кельвинов в градусы Цельсия."""
    return subtract(k, 273.15)


def celsius_to_fahrenheit(c):
    """Переводит температуру из градусов Цельсия в градусы Фаренгейта."""
    return add(divide(multiply(c, 9), 5), 32)


def fahrenheit_to_celsius(f):
    """Переводит температуру из градусов Фаренгейта в градусы Цельсия."""
    return divide(multiply(subtract(f, 32), 5), 9)


def is_temperature_unit(name):
    """Возвращает True, если name — единица температуры: c, f, k."""
    return name in TEMPERATURE_UNITS


def to_celsius(x, from_unit):
    """Переводит температуру x в градусы Цельсия из единицы from_unit: c, f или k."""
    if not is_temperature_unit(from_unit):
        raise ValueError("Неизвестная единица температуры: '" + str(from_unit) + "'.")
    if from_unit == "f":
        return fahrenheit_to_celsius(x)
    if from_unit == "k":
        return kelvin_to_celsius(x)
    return x


def from_celsius(c, to_unit):
    """Переводит температуру c из градусов Цельсия в единицу to_unit: c, f или k."""
    if not is_temperature_unit(to_unit):
        raise ValueError("Неизвестная единица температуры: '" + str(to_unit) + "'.")
    if to_unit == "f":
        return celsius_to_fahrenheit(c)
    if to_unit == "k":
        return celsius_to_kelvin(c)
    return c


def convert_temperature(x, from_unit, to_unit):
    """Переводит температуру x между единицами c, f и k через градусы Цельсия."""
    return from_celsius(to_celsius(x, from_unit), to_unit)


def convert_unit(x, from_unit, to_unit):
    """Главная функция части 2: переводит число x между любыми единицами одной категории."""
    if is_length_unit(from_unit) and is_length_unit(to_unit):
        return convert_length(x, from_unit, to_unit)
    if is_mass_unit(from_unit) and is_mass_unit(to_unit):
        return convert_mass(x, from_unit, to_unit)
    if is_volume_unit(from_unit) and is_volume_unit(to_unit):
        return convert_volume(x, from_unit, to_unit)
    if is_temperature_unit(from_unit) and is_temperature_unit(to_unit):
        return convert_temperature(x, from_unit, to_unit)
    raise ValueError("Единицы '" + str(from_unit) + "' и '" + str(to_unit)
                     + "' несовместимы или неизвестны.")