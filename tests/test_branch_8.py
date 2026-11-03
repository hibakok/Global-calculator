# Тесты Ветви 8. Преобразования: системы счисления 2-36.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_8_conversions import (
    digit_char, digit_value, check_base, check_integer,
    is_base_digit, check_base_digit, to_base_values, values_to_string,
    to_base_positive, to_base_string, split_sign, from_base_digits,
    from_base_string, convert_base,
)


class TestDigitChar(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(digit_char(0), "0")

    def test_nine(self):
        self.assertEqual(digit_char(9), "9")

    def test_ten(self):
        self.assertEqual(digit_char(10), "a")

    def test_max(self):
        self.assertEqual(digit_char(35), "z")

    def test_too_big(self):
        with self.assertRaises(ValueError):
            digit_char(36)

    def test_negative(self):
        with self.assertRaises(ValueError):
            digit_char(-1)


class TestDigitValue(unittest.TestCase):
    def test_digit(self):
        self.assertEqual(digit_value("7"), 7)

    def test_letter(self):
        self.assertEqual(digit_value("a"), 10)

    def test_uppercase(self):
        self.assertEqual(digit_value("Z"), 35)

    def test_zero(self):
        self.assertEqual(digit_value("0"), 0)

    def test_not_a_digit(self):
        with self.assertRaises(ValueError):
            digit_value("!")

    def test_cyrillic_letter(self):
        with self.assertRaises(ValueError):
            digit_value("я")

    def test_empty(self):
        with self.assertRaises(ValueError):
            digit_value("")

    def test_two_chars(self):
        with self.assertRaises(ValueError):
            digit_value("10")


class TestCheckBase(unittest.TestCase):
    def test_min(self):
        self.assertEqual(check_base(2), 2)

    def test_max(self):
        self.assertEqual(check_base(36), 36)

    def test_middle(self):
        self.assertEqual(check_base(16), 16)

    def test_too_small(self):
        with self.assertRaises(ValueError):
            check_base(1)

    def test_too_big(self):
        with self.assertRaises(ValueError):
            check_base(37)

    def test_not_int(self):
        with self.assertRaises(TypeError):
            check_base("16")


class TestCheckInteger(unittest.TestCase):
    def test_int(self):
        self.assertEqual(check_integer(5), 5)

    def test_negative(self):
        self.assertEqual(check_integer(-3), -3)

    def test_float(self):
        with self.assertRaises(TypeError):
            check_integer(2.5)

    def test_string(self):
        with self.assertRaises(TypeError):
            check_integer("5")


class TestIsBaseDigit(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_base_digit("1", 2))

    def test_invalid_for_binary(self):
        self.assertFalse(is_base_digit("2", 2))

    def test_letter_valid(self):
        self.assertTrue(is_base_digit("f", 16))

    def test_letter_invalid(self):
        self.assertFalse(is_base_digit("g", 16))

    def test_uppercase(self):
        self.assertTrue(is_base_digit("F", 16))

    def test_empty(self):
        self.assertFalse(is_base_digit("", 16))

    def test_not_a_digit(self):
        self.assertFalse(is_base_digit("!", 16))


class TestCheckBaseDigit(unittest.TestCase):
    def test_returns_value(self):
        self.assertEqual(check_base_digit("7", 10), 7)

    def test_letter(self):
        self.assertEqual(check_base_digit("a", 16), 10)

    def test_digit_too_big(self):
        with self.assertRaises(ValueError):
            check_base_digit("9", 8)

    def test_not_a_digit(self):
        with self.assertRaises(ValueError):
            check_base_digit("x", 10)


class TestToBaseValues(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(to_base_values(0, 2), [0])

    def test_five_binary(self):
        self.assertEqual(to_base_values(5, 2), [1, 0, 1])

    def test_255_hex(self):
        self.assertEqual(to_base_values(255, 16), [15, 15])

    def test_single(self):
        self.assertEqual(to_base_values(7, 10), [7])

    def test_negative(self):
        with self.assertRaises(ValueError):
            to_base_values(-1, 2)


class TestValuesToString(unittest.TestCase):
    def test_binary(self):
        self.assertEqual(values_to_string([1, 0, 1]), "101")

    def test_hex(self):
        self.assertEqual(values_to_string([15, 15]), "ff")

    def test_zero(self):
        self.assertEqual(values_to_string([0]), "0")

    def test_empty(self):
        self.assertEqual(values_to_string([]), "")

    def test_bad_value(self):
        with self.assertRaises(ValueError):
            values_to_string([36])


class TestToBasePositive(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(to_base_positive(0, 2), "0")

    def test_binary(self):
        self.assertEqual(to_base_positive(5, 2), "101")

    def test_hex(self):
        self.assertEqual(to_base_positive(255, 16), "ff")

    def test_base36(self):
        self.assertEqual(to_base_positive(35, 36), "z")

    def test_decimal(self):
        self.assertEqual(to_base_positive(10, 10), "10")


class TestToBaseString(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(to_base_string(255, 16), "ff")

    def test_negative(self):
        self.assertEqual(to_base_string(-255, 16), "-ff")

    def test_zero(self):
        self.assertEqual(to_base_string(0, 2), "0")

    def test_negative_one(self):
        self.assertEqual(to_base_string(-1, 36), "-1")

    def test_bad_base(self):
        with self.assertRaises(ValueError):
            to_base_string(5, 1)

    def test_float_number(self):
        with self.assertRaises(TypeError):
            to_base_string(2.5, 2)


class TestSplitSign(unittest.TestCase):
    def test_no_sign(self):
        self.assertEqual(split_sign("ff"), (1, "ff"))

    def test_minus(self):
        self.assertEqual(split_sign("-ff"), (-1, "ff"))

    def test_plus(self):
        self.assertEqual(split_sign("+ff"), (1, "ff"))

    def test_spaces(self):
        self.assertEqual(split_sign("  - ff "), (-1, "ff"))

    def test_empty(self):
        with self.assertRaises(ValueError):
            split_sign("")

    def test_spaces_only(self):
        with self.assertRaises(ValueError):
            split_sign("   ")

    def test_not_a_string(self):
        with self.assertRaises(TypeError):
            split_sign(255)


class TestFromBaseDigits(unittest.TestCase):
    def test_binary(self):
        self.assertEqual(from_base_digits("101", 2), 5)

    def test_hex(self):
        self.assertEqual(from_base_digits("ff", 16), 255)

    def test_uppercase(self):
        self.assertEqual(from_base_digits("FF", 16), 255)

    def test_zero(self):
        self.assertEqual(from_base_digits("0", 2), 0)

    def test_empty(self):
        self.assertEqual(from_base_digits("", 16), 0)

    def test_digit_too_big(self):
        with self.assertRaises(ValueError):
            from_base_digits("8", 8)

    def test_not_a_digit(self):
        with self.assertRaises(ValueError):
            from_base_digits("x", 10)


class TestFromBaseString(unittest.TestCase):
    def test_binary(self):
        self.assertEqual(from_base_string("101", 2), 5)

    def test_hex(self):
        self.assertEqual(from_base_string("ff", 16), 255)

    def test_uppercase(self):
        self.assertEqual(from_base_string("FF", 16), 255)

    def test_negative(self):
        self.assertEqual(from_base_string("-ff", 16), -255)

    def test_plus(self):
        self.assertEqual(from_base_string("+ff", 16), 255)

    def test_spaces(self):
        self.assertEqual(from_base_string("  ff ", 16), 255)

    def test_base36(self):
        self.assertEqual(from_base_string("z", 36), 35)

    def test_zero(self):
        self.assertEqual(from_base_string("0", 2), 0)

    def test_leading_zeros(self):
        self.assertEqual(from_base_string("007", 10), 7)

    def test_big_power_of_two(self):
        self.assertEqual(from_base_string("1" + "0" * 64, 2), 2 ** 64)

    def test_empty(self):
        with self.assertRaises(ValueError):
            from_base_string("", 16)

    def test_sign_only(self):
        with self.assertRaises(ValueError):
            from_base_string("-", 16)

    def test_space_inside(self):
        with self.assertRaises(ValueError):
            from_base_string("f f", 16)

    def test_digit_too_big(self):
        with self.assertRaises(ValueError):
            from_base_string("8", 8)

    def test_bad_base(self):
        with self.assertRaises(ValueError):
            from_base_string("101", 1)

    def test_not_a_string(self):
        with self.assertRaises(TypeError):
            from_base_string(101, 2)


class TestConvertBase(unittest.TestCase):
    def test_hex_to_binary(self):
        self.assertEqual(convert_base("ff", 16, 2), "11111111")

    def test_binary_to_decimal(self):
        self.assertEqual(convert_base("1010", 2, 10), "10")

    def test_negative(self):
        self.assertEqual(convert_base("-ff", 16, 10), "-255")

    def test_same_base(self):
        self.assertEqual(convert_base("123", 10, 10), "123")

    def test_zero(self):
        self.assertEqual(convert_base("0", 10, 2), "0")

    def test_uppercase(self):
        self.assertEqual(convert_base("FF", 16, 10), "255")

    def test_bad_digit(self):
        with self.assertRaises(ValueError):
            convert_base("8", 8, 10)

    def test_bad_target_base(self):
        with self.assertRaises(ValueError):
            convert_base("10", 10, 37)


if __name__ == "__main__":
    unittest.main()