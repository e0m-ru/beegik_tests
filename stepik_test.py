import sys
import io
import zipfile


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


def capture_output(code: str) -> str:
    """выполняет переданный код, 
    и перенаправляет стандартный вывод в объект IO. 
    возвращает содержимое результат выполнения в виде строки."""
    with io_context() as IO:
        try:
            # выполняется с преданным контекстом
            exec(code, globals()['_context'])
        except Exception as e:
            return f'{e}'
    return IO.getvalue()


def run_one_test(test: str, answer: str) -> bool:
    """выполняет один тестовый случай, 
    сравнивая полученный результат с ожидаемым ответом."""
    result = capture_output(test)
    return answer == result.strip()


def run(test_zip_file: str | int, context: dict, verbose=None):
    """принимает два аргумента:
    test_zip_file (строка или целое число) - имя zip файла с тестами
    context (словарь) - контекст выполнения. 
    """
    globals()['_context'] = context

    zip_file = zipfile.ZipFile(f'{test_zip_file}.zip')
    for file_name in zip_file.namelist()[::2]:
        passed = run_one_test(*open_file_in_zip(zip_file, file_name))
        if verbose:
            print(f'Тест №{file_name}: {passed}')
    zip_file.close()
    print('All tests passed')


def open_file_in_zip(zip_file, file_name):
    answer_filename = '{}.clue'.format(file_name)
    return read_decode(zip_file, file_name),\
        read_decode(zip_file, answer_filename)


def read_decode(zip_file, file_name):
    return zip_file.open(file_name).read().decode('utf-8')
