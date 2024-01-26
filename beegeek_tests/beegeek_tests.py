import io
import sys
import os
import zipfile
from colorama import Fore
import traceback
# from config import *


class Test:
    def __init__(self, name: str, code, expected: str) -> None:
        self.name, self.code, self.expected = name, code, expected
        self.result: str | None = None
        self.status: bool | None = None


class Test_manager:
    """Принимает два аргумента:\n
        test_zip - путь к zip файлу с тестами\n
        context - контекст выполнения (globals() например)"""

    def __init__(self, test_zip: str, context: dict = dict()) -> None:
        self.tests_files = zipfile.ZipFile(test_zip)
        self._context = context

    @classmethod
    def capture_exec_output(cls, test: Test, context: dict) -> str:
        """выполняет переданный код, 
        и перенаправляет стандартный вывод в объект IO. 
        возвращает строку результата выполнения."""
        with io_context() as IO:
            try:
                exec(test.code, context)
            except Exception as e:

                return traceback.format_exc()
            return IO.getvalue().strip()

    def run(self, number=None, _verbose=False, _traceback=True, _code=False):
        "Запускает все тесты из архива."
        os.system('cls' if os.name == 'nt' else 'clear')
        if number:
            i = range(number, number+1)
        else:
            i = range(1, (len(self.tests_files.filelist)//2)+1)
        for n in i:
            code = self.tests_files.read(f'{n}')
            expected = self.tests_files.read(
                f'{n}.clue').decode('utf_8')
            t = Test(str(n), code, expected)
            self.run_test(t)
            self.__setattr__(f'{n}', t)

            if self.__dict__[f'{n}'].status is False:
                print(f'Test №{n}: {Fore.RED}failed{Fore.WHITE}')
                if _verbose:
                    print(f'{Fore.RED}{"result":-^24}')
                    print(
                        f"{self.__dict__[str(n)].result if _traceback else ''}")
                    print(f'{Fore.YELLOW}{"answer":-^24}')
                    print(f"{self.__dict__[str(n)].expected}{Fore.WHITE}")
                if _code:
                    print(f'{Fore.BLUE}{"code":-^24}')
                    message = self.__dict__[str(n)].code.decode("utf_8")
                    print(f'{message}{Fore.WHITE}')
                    print(f"{'':-^24}\n")
            else:
                print(f'Тест №{n}: {Fore.GREEN}passed{Fore.WHITE}')

    def run_test(self, t: Test):
        t.result = self.capture_exec_output(t, self._context)
        t.status = t.expected == t.result


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
