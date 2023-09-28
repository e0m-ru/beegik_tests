import sys
import io


class io_context:
    """Контекстный менеджер
    Перенаправляет стандартный вывод в строку"""

    def __init__(self) -> None:
        self.captured_output = io.StringIO()

    def __enter__(self):
        sys.stdout = self.captured_output
        return self.captured_output

    def __exit__(self, *args):
        sys.stdout = sys.__stdout__
        return self.captured_output.getvalue()


def capture_output(code: str, context) -> str:
    """выполняет переданный код, 
    и перенаправляет стандартный вывод в объект IO. 
    возвращает содержимое результат выполнения в виде строки."""
    with io_context() as IO:
        try:
            exec(code, context)
        except Exception as e:
            return e
        return IO.getvalue().strip()
