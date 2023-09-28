import io
import sys
import zipfile
from colorama import Fore


class Test_manager:
    """Принимает два аргумента:\n
        test_zip - путь к zip файлу с тестами\n
        context - контекст выполнения (globals() например)"""

    def __init__(self, test_zip: str, context: dict = dict) -> None:
        self.tests_files = zipfile.ZipFile(test_zip)
        self._context = context

    @classmethod
    def capture_exec_output(self, code: str) -> str:
        """выполняет переданный код, 
        и перенаправляет стандартный вывод в объект IO. 
        возвращает строку результата выполнения."""
        with io_context() as IO:
            try:
                exec(code, self._context)
            except Exception as e:
                return e
            return IO.getvalue().strip()

    class Test:
        def __init__(self, code: str, expected: str) -> None:
            self.code = code
            self.expected = expected
            self.status = self.result == self.expected

        @property
        def result(self):
            self._result = Test_manager.capture_exec_output(self.code)
            return self._result

    def run(self):
        """Запускает все тесты из архива.
        """
        for test_number in range(1, (len(self.tests_files.filelist)//2)+1):
            code = self.tests_files.read(f'{test_number}')
            expected = self.tests_files.read(
                f'{test_number}.clue').decode('utf_8')
            self.__setattr__(str(test_number), self.Test(code, expected))
            if self.__dict__[str(test_number)].status is False:
                print(
                    f'{Fore.RED}Failed on test № {test_number}{Fore.WHITE}\nresult:\n{self.__dict__[str(test_number)].result}\nanswer:\n{self.__dict__[str(test_number)].expected}')
                break
            print(f'Тест №{test_number}: {Fore.GREEN}passed{Fore.WHITE}')

    def run_test(self, test_number: int) -> str:
        """выполняет один тестовый случай, 
        возвращает полученный результат"""

    @staticmethod
    def open_file_in_zip(tests_files, test_number):
        answer_filename = '{}.clue'.format(test_number)
        return Test_manager.read_decode(tests_files, test_number),\
            Test_manager.read_decode(tests_files, answer_filename)

    @staticmethod
    def read_decode(tests_files, test_number):
        return tests_files.open(test_number).read().decode('utf-8')


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
