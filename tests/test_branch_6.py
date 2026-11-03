# Тесты Ветви 6. Научные выражения.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_6_scientific_expressions import (
    is_letter, read_name, is_exponent_letter, has_exponent,
    exponent_digits_start, read_number_exp, read_token_scientific,
    tokenize_with, tokenize_scientific,
)
from branch_3a_tokenizer import read_token, tokenize


class TestIsLetter(unittest.TestCase):
    def test_lower(self):
        self.assertTrue(is_letter("a"))

    def test_upper(self):
        self.assertTrue(is_letter("Z"))

    def test_digit(self):
        self.assertFalse(is_letter("5"))

    def test_operator(self):
        self.assertFalse(is_letter("+"))

    def test_cyrillic(self):
        self.assertFalse(is_letter("п"))


class TestReadName(unittest.TestCase):
    def test_name(self):
        self.assertEqual(read_name("sqrt(2)", 0), 4)

    def test_single_letter(self):
        self.assertEqual(read_name("e + 1", 0), 1)

    def test_stops_at_digit(self):
        self.assertEqual(read_name("sin2", 0), 3)

    def test_stops_at_space(self):
        self.assertEqual(read_name("pi e", 0), 2)

    def test_not_letter(self):
        self.assertEqual(read_name("2 + 2", 0), 0)


class TestIsExponentLetter(unittest.TestCase):
    def test_lower(self):
        self.assertTrue(is_exponent_letter("e"))

    def test_upper(self):
        self.assertTrue(is_exponent_letter("E"))

    def test_other_letter(self):
        self.assertFalse(is_exponent_letter("a"))

    def test_digit(self):
        self.assertFalse(is_exponent_letter("3"))


class TestHasExponent(unittest.TestCase):
    def test_digit_after(self):
        self.assertTrue(has_exponent("1e3", 1))

    def test_sign_minus(self):
        self.assertTrue(has_exponent("1e-4", 1))

    def test_sign_plus(self):
        self.assertTrue(has_exponent("1e+4", 1))

    def test_upper(self):
        self.assertTrue(has_exponent("1E3", 1))

    def test_lone_letter(self):
        self.assertFalse(has_exponent("1e", 1))

    def test_letter_at_end(self):
        self.assertFalse(has_exponent("12e", 2))

    def test_sign_without_digits(self):
        self.assertFalse(has_exponent("1e-", 1))

    def test_not_exponent_letter(self):
        self.assertFalse(has_exponent("1a3", 1))


class TestExponentDigitsStart(unittest.TestCase):
    def test_without_sign(self):
        self.assertEqual(exponent_digits_start("1e3", 1), 2)

    def test_after_minus(self):
        self.assertEqual(exponent_digits_start("1e-3", 1), 3)

    def test_after_plus(self):
        self.assertEqual(exponent_digits_start("1e+3", 1), 3)


class TestReadNumberExp(unittest.TestCase):
    def test_plain_int(self):
        self.assertEqual(read_number_exp("42 + 1", 0), (42, 2))

    def test_plain_float(self):
        self.assertEqual(read_number_exp("3.14", 0), (3.14, 4))

    def test_exponent(self):
        self.assertEqual(read_number_exp("1e3", 0), (1000.0, 3))

    def test_fraction_with_negative_exponent(self):
        self.assertEqual(read_number_exp("2.5e-4", 0), (0.00025, 6))

    def test_upper_with_plus(self):
        self.assertEqual(read_number_exp("1E+2", 0), (100.0, 4))

    def test_lone_letter_is_not_exponent(self):
        self.assertEqual(read_number_exp("2e", 0), (2, 1))

    def test_huge_exponent_overflow(self):
        self.assertEqual(read_number_exp("1e400", 0), (float("inf"), 5))

    def test_tiny_exponent_underflow(self):
        self.assertEqual(read_number_exp("1e-400", 0), (0.0, 6))


class TestReadTokenScientific(unittest.TestCase):
    def test_name(self):
        self.assertEqual(read_token_scientific("sqrt", 0), (("name", "sqrt"), 4))

    def test_number_with_exponent(self):
        self.assertEqual(read_token_scientific("1e3", 0), (("number", 1000.0), 3))

    def test_operator(self):
        self.assertEqual(read_token_scientific("^", 0), (("operator", "^"), 1))

    def test_left_paren(self):
        self.assertEqual(read_token_scientific("(", 0), (("left_paren", "("), 1))

    def test_right_paren(self):
        self.assertEqual(read_token_scientific(")", 0), (("right_paren", ")"), 1))

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            read_token_scientific("#", 0)


class TestTokenizeWith(unittest.TestCase):
    def test_same_as_tokenize(self):
        self.assertEqual(tokenize_with("1 + 2 * 3", read_token),
                         tokenize("1 + 2 * 3"))

    def test_skips_spaces(self):
        self.assertEqual(tokenize_with("  pi", read_token_scientific),
                         [("name", "pi")])


class TestTokenizeScientific(unittest.TestCase):
    def test_full_expression(self):
        self.assertEqual(
            tokenize_scientific("sqrt(2) + sin(pi/2)"),
            [("name", "sqrt"), ("left_paren", "("), ("number", 2),
             ("right_paren", ")"), ("operator", "+"), ("name", "sin"),
             ("left_paren", "("), ("name", "pi"), ("operator", "/"),
             ("number", 2), ("right_paren", ")")])

    def test_exponent_number(self):
        self.assertEqual(tokenize_scientific("1e3 * 2"),
                         [("number", 1000.0), ("operator", "*"),
                          ("number", 2)])

    def test_number_then_constant(self):
        self.assertEqual(tokenize_scientific("2e"),
                         [("number", 2), ("name", "e")])

    def test_empty(self):
        self.assertEqual(tokenize_scientific(""), [])

    def test_spaces_only(self):
        self.assertEqual(tokenize_scientific("   "), [])

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            tokenize_scientific("2 # 3")


if __name__ == "__main__":
    unittest.main()