# Тесты Ветви 3a. Разбор выражений: токенизатор.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_3a_tokenizer import (
    is_digit, is_space, is_operator, skip_spaces,
    read_digits, read_number, make_token, read_token, tokenize,
)


class TestIsDigit(unittest.TestCase):
    def test_digits(self):
        self.assertTrue(is_digit("0"))
        self.assertTrue(is_digit("7"))

    def test_not_digits(self):
        self.assertFalse(is_digit("a"))
        self.assertFalse(is_digit("."))
        self.assertFalse(is_digit(" "))


class TestIsSpace(unittest.TestCase):
    def test_spaces(self):
        self.assertTrue(is_space(" "))
        self.assertTrue(is_space("\t"))
        self.assertTrue(is_space("\n"))

    def test_not_spaces(self):
        self.assertFalse(is_space("0"))
        self.assertFalse(is_space("+"))


class TestIsOperator(unittest.TestCase):
    def test_operators(self):
        for op in "+-*/%^":
            self.assertTrue(is_operator(op))

    def test_not_operators(self):
        self.assertFalse(is_operator("("))
        self.assertFalse(is_operator("2"))


class TestSkipSpaces(unittest.TestCase):
    def test_no_spaces(self):
        self.assertEqual(skip_spaces("2+2", 0), 0)

    def test_spaces_inside(self):
        # "2 + 2": индекс 1 — пробел, индекс 2 — знак «+».
        self.assertEqual(skip_spaces("2 + 2", 1), 2)

    def test_only_spaces(self):
        self.assertEqual(skip_spaces("   ", 0), 3)


class TestReadDigits(unittest.TestCase):
    def test_digits(self):
        self.assertEqual(read_digits("123+", 0), 3)

    def test_no_digits(self):
        self.assertEqual(read_digits("+123", 0), 0)


class TestReadNumber(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(read_number("123+", 0), (123, 3))

    def test_float(self):
        self.assertEqual(read_number("3.14)", 0), (3.14, 4))

    def test_dot_without_digits_not_consumed(self):
        # Точка без цифры после неё не является частью числа.
        self.assertEqual(read_number("5.", 0), (5, 1))

    def test_result_type(self):
        value, _ = read_number("42", 0)
        self.assertIsInstance(value, int)
        value, _ = read_number("4.2", 0)
        self.assertIsInstance(value, float)


class TestMakeToken(unittest.TestCase):
    def test_token_is_pair(self):
        self.assertEqual(make_token("number", 5), ("number", 5))


class TestReadToken(unittest.TestCase):
    def test_number(self):
        self.assertEqual(read_token("10+", 0), (("number", 10), 2))

    def test_operator(self):
        self.assertEqual(read_token("+10", 0), (("operator", "+"), 1))

    def test_parens(self):
        self.assertEqual(read_token("(1", 0), (("left_paren", "("), 1))
        self.assertEqual(read_token(")1", 0), (("right_paren", ")"), 1))

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            read_token("a1", 0)


class TestTokenize(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(
            tokenize("2+2"),
            [("number", 2), ("operator", "+"), ("number", 2)],
        )

    def test_spaces_ignored(self):
        self.assertEqual(tokenize(" 1 + 2 * 3 "), tokenize("1+2*3"))

    def test_float_and_parens(self):
        self.assertEqual(
            tokenize("(1.5+2)"),
            [("left_paren", "("), ("number", 1.5), ("operator", "+"),
             ("number", 2), ("right_paren", ")")],
        )

    def test_empty(self):
        self.assertEqual(tokenize(""), [])

    def test_only_spaces(self):
        self.assertEqual(tokenize("  "), [])

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            tokenize("2 + a")


if __name__ == "__main__":
    unittest.main()
