# Ветвь 9. Консольный интерфейс.
# Часть 1 — цикл ввода: читает строку, вычисляет её в сессии
# (переменные, ans, история) и печатает результат; пустые строки
# пропускаются, ошибки выводятся сообщением, а не падением.
# Часть 2 — справка и понятный вывод ошибок: команда help
# (также справка и ?) печатает справку по командам, выражениям,
# функциям и переменным; глубоко вложенные скобки дают понятное
# сообщение вместо падения цикла. Команда справки проверяется
# по всей строке, поэтому присваивание "help = 5" работает.
# Выход — команда exit, quit, выход или конец ввода (Ctrl+D).
# Собирается из методов Ветви 7 (make_session, calculate_session).

from branch_7_memory import make_session, calculate_session

EXIT_COMMANDS = ("exit", "quit", "выход")
HELP_COMMANDS = ("help", "справка", "?")
PROMPT = "> "
GREETING = "Global Calculator. Введите выражение; help — справка, exit — выход."
RESULT_PREFIX = "= "
ERROR_PREFIX = "Ошибка: "


def is_exit_command(line):
    """Возвращает True, если строка line — команда выхода: exit, quit или выход."""
    return line.strip().lower() in EXIT_COMMANDS


def is_help_command(line):
    """Возвращает True, если строка line — команда справки: help, справка или ?."""
    return line.strip().lower() in HELP_COMMANDS


def is_blank(line):
    """Возвращает True, если строка line пустая или состоит из одних пробелов."""
    return line.strip() == ""


def help_commands_text():
    """Возвращает раздел справки о командах программы."""
    return ("Команды:\n"
            "  help, справка, ?  — показать эту справку\n"
            "  exit, quit, выход — завершить работу")


def help_syntax_text():
    """Возвращает раздел справки о записи выражений."""
    return ("Выражения:\n"
            "  числа: 42, 3.14, 1e3, 2.5e-2\n"
            "  операции: + - * / % (остаток); ^ — степень\n"
            "  скобки: (2 + 2) * 3; унарные знаки: -2, +2\n"
            "  приоритет: ^ выше * / %, те выше + -;\n"
            "  степень считается справа налево: 2^3^2 = 512")


def help_functions_text():
    """Возвращает раздел справки о функциях и константах."""
    return ("Функции (углы — в радианах):\n"
            "  sqrt(x), exp(x), ln(x), sin(x), cos(x), tan(x)\n"
            "Константы:\n"
            "  pi, e")


def help_variables_text():
    """Возвращает раздел справки о переменных и ans."""
    return ("Переменные:\n"
            "  x = 2 + 2  — присваивание (имя из латинских букв)\n"
            "  a = b = 2  — цепочка присваиваний\n"
            "  x * 3      — использование переменной\n"
            "  ans        — последний результат: ans * 2")


def help_text():
    """Возвращает полный текст справки: разделы, соединённые пустой строкой."""
    parts = (help_commands_text(), help_syntax_text(),
             help_functions_text(), help_variables_text())
    return "\n\n".join(parts)


def format_value(value):
    """Форматирует число для вывода: целые float без точки, прочее — str."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def result_text(value):
    """Возвращает текст успешного результата: '= ' и отформатированное число."""
    return RESULT_PREFIX + format_value(value)


def explain_error(error):
    """Переводит исключение error в понятное сообщение на русском языке."""
    if isinstance(error, RecursionError):
        return "Слишком глубокая вложенность скобок или функций."
    return str(error)


def error_text(error):
    """Возвращает текст сообщения об ошибке: 'Ошибка: ' и понятное сообщение."""
    return ERROR_PREFIX + explain_error(error)


def line_output(line, session):
    """Возвращает строку-ответ на строку ввода (результат, справка или ошибка) либо None для пустой строки."""
    if is_blank(line):
        return None
    if is_help_command(line):
        return help_text()
    try:
        value = calculate_session(line, session)
    except (ValueError, TypeError, ArithmeticError, RecursionError) as error:
        return error_text(error)
    return result_text(value)


def read_line():
    """Читает строку ввода с приглашением; при конце ввода или прерывании возвращает None."""
    try:
        return input(PROMPT)
    except (EOFError, KeyboardInterrupt):
        return None


def run_repl(session):
    """Запускает цикл ввода-ответа; команду выхода и конец ввода обрабатывает молча."""
    while True:
        line = read_line()
        if line is None or is_exit_command(line):
            return
        output = line_output(line, session)
        if output is not None:
            print(output)


def main():
    """Запускает калькулятор целиком: приветствие, сессия и цикл ввода."""
    print(GREETING)
    run_repl(make_session())