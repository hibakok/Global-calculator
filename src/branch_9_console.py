# Ветвь 9. Консольный интерфейс.
# Часть 1 — цикл ввода: читает строку, вычисляет её в сессии
# (переменные, ans, история) и печатает результат; пустые строки
# пропускаются, ошибки выводятся сообщением, а не падением.
# Выход — команда exit, quit, выход или конец ввода (Ctrl+D).
# Собирается из методов Ветви 7 (make_session, calculate_session).

from branch_7_memory import make_session, calculate_session

EXIT_COMMANDS = ("exit", "quit", "выход")
PROMPT = "> "
GREETING = "Global Calculator. Введите выражение; exit или выход — завершить."
RESULT_PREFIX = "= "
ERROR_PREFIX = "Ошибка: "


def is_exit_command(line):
    """Возвращает True, если строка line — команда выхода: exit, quit или выход."""
    return line.strip().lower() in EXIT_COMMANDS


def is_blank(line):
    """Возвращает True, если строка line пустая или состоит из одних пробелов."""
    return line.strip() == ""


def format_value(value):
    """Форматирует число для вывода: целые float без точки, прочее — str."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def result_text(value):
    """Возвращает текст успешного результата: '= ' и отформатированное число."""
    return RESULT_PREFIX + format_value(value)


def error_text(error):
    """Возвращает текст сообщения об ошибке: 'Ошибка: ' и сообщение исключения."""
    return ERROR_PREFIX + str(error)


def line_output(line, session):
    """Возвращает строку-ответ на строку ввода (результат или ошибка) либо None для пустой строки."""
    if is_blank(line):
        return None
    try:
        value = calculate_session(line, session)
    except (ValueError, TypeError, ArithmeticError) as error:
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