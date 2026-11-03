# Тесты ветви 9: консольный интерфейс, часть 1 — цикл ввода.
# На каждый метод: обычный, граничный и ошибочный случай
# (у методов без исключений третий случай — ещё одна граница).
# Цикл ввода проверяется подменой builtins.input и перехватом
# вывода через contextlib.redirect_stdout — только стандартная
# библиотека.

import builtins
import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_7_memory import make_session
from branch_9_console import (
    is_exit_command, is_blank, format_value, result_text, error_text,
    line_output, read_line, run_repl, main,
)


class FakeInput:
    """Подмена builtins.input: выдаёт строки по очереди, затем конец ввода."""

    def __init__(self, lines):
        self.lines = list(lines)

    def __call__(self, prompt=""):
        if not self.lines:
            raise EOFError
        return self.lines.pop(0)


def run_with_inputs(lines, session):
    """Запускает run_repl с подменённым input; возвращает перехваченный вывод."""
    original_input = builtins.input
    builtins.input = FakeInput(lines)
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            run_repl(session)
    finally:
        builtins.input = original_input
    return buffer.getvalue()


def run_main_with_inputs(lines):
    """Запускает main с подменённым input; возвращает перехваченный вывод."""
    original_input = builtins.input
    builtins.input = FakeInput(lines)
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            main()
    finally:
        builtins.input = original_input
    return buffer.getvalue()


class TestIsExitCommand(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(is_exit_command("exit"), True)

    def test_boundary(self):
        self.assertEqual(is_exit_command("  ВЫХОД  "), True)
        self.assertEqual(is_exit_command("Quit"), True)

    def test_error(self):
        self.assertEqual(is_exit_command("2 + 2"), False)
        self.assertEqual(is_exit_command(""), False)


class TestIsBlank(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(is_blank("   "), True)

    def test_boundary(self):
        self.assertEqual(is_blank(""), True)
        self.assertEqual(is_blank("\t  "), True)

    def test_error(self):
        self.assertEqual(is_blank("2 + 2"), False)


class TestFormatValue(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(format_value(4.0), "4")

    def test_boundary(self):
        self.assertEqual(format_value(2.5), "2.5")
        self.assertEqual(format_value(-7), "-7")

    def test_error(self):
        self.assertEqual(format_value(2.5 * 2), "5")


class TestResultText(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(result_text(4.0), "= 4")

    def test_boundary(self):
        self.assertEqual(result_text(0.5), "= 0.5")

    def test_error(self):
        self.assertEqual(result_text(-3), "= -3")


class TestErrorText(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(error_text(ValueError("тест")), "Ошибка: тест")

    def test_boundary(self):
        self.assertEqual(error_text(ZeroDivisionError("Деление на ноль запрещено.")),
                         "Ошибка: Деление на ноль запрещено.")

    def test_error(self):
        self.assertTrue(error_text(ValueError("")).startswith("Ошибка: "))


class TestLineOutput(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(line_output("2 + 2", make_session()), "= 4")

    def test_boundary(self):
        session = make_session()
        self.assertEqual(line_output("x = 2 + 2", session), "= 4")
        self.assertEqual(line_output("x * 3", session), "= 12")
        self.assertEqual(line_output("ans + 1", session), "= 13")
        self.assertEqual(line_output("   ", session), None)

    def test_error(self):
        session = make_session()
        self.assertEqual(line_output("1 / 0", session),
                         "Ошибка: Деление на ноль запрещено.")
        self.assertEqual(line_output("2 +", session),
                         "Ошибка: Ожидалось число, имя, открывающая скобка или унарный знак.")


class TestReadLine(unittest.TestCase):
    def test_usual(self):
        original_input = builtins.input
        builtins.input = FakeInput(["2 + 2"])
        try:
            self.assertEqual(read_line(), "2 + 2")
        finally:
            builtins.input = original_input

    def test_boundary(self):
        original_input = builtins.input
        builtins.input = FakeInput([])
        try:
            self.assertEqual(read_line(), None)
        finally:
            builtins.input = original_input

    def test_error(self):
        def interrupted(prompt=""):
            raise KeyboardInterrupt
        original_input = builtins.input
        builtins.input = interrupted
        try:
            self.assertEqual(read_line(), None)
        finally:
            builtins.input = original_input


class TestRunRepl(unittest.TestCase):
    def test_usual(self):
        output = run_with_inputs(["2 + 2", "exit"], make_session())
        self.assertIn("= 4", output)

    def test_boundary(self):
        self.assertEqual(run_with_inputs([], make_session()), "")
        output = run_with_inputs(["   ", "sqrt(2) * 0", "выход"], make_session())
        self.assertIn("= 0", output)
        self.assertNotIn("= 4", output)

    def test_error(self):
        output = run_with_inputs(["1 / 0", "2 + 2", "exit"], make_session())
        self.assertIn("Ошибка: Деление на ноль запрещено.", output)
        self.assertIn("= 4", output)


class TestMain(unittest.TestCase):
    def test_usual(self):
        output = run_main_with_inputs(["2 + 2 * 2", "exit"])
        self.assertIn("Global Calculator", output)
        self.assertIn("= 6", output)

    def test_boundary(self):
        output = run_main_with_inputs(["exit"])
        self.assertIn("Global Calculator", output)

    def test_error(self):
        output = run_main_with_inputs(["ln(0)", "exit"])
        self.assertIn("Ошибка: Логарифм определён только для положительных чисел.", output)


if __name__ == "__main__":
    unittest.main()