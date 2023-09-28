from .helpers import *
import zipfile
from colorama import Fore


def run_one_test(test: str, answer: str, context: dict) -> bool:
    """выполняет один тестовый случай, 
    возвращает полученный результат и ожидаемый ответ."""
    result = capture_output(test, context)
    return answer == result, result, answer


def run(test_zip: str | int, context: dict):
    """Запускает все тесты из архива.
    Принимает два аргумента:\n
    test_zip - путь к zip файлу с тестами\n
    context - контекст выполнения (globals() например)
    """
    tests_files = zipfile.ZipFile(f'{test_zip}')

    for file_name in tests_files.namelist()[::2]:
        exec_results = run_one_test(
            *open_file_in_zip(tests_files, file_name), context)
        if exec_results[0] is False:
            test_number = file_name
            print(
                f'{Fore.RED}Failed on test № {file_name}{Fore.WHITE}\nresult:\n{exec_results[1]}\nanswer:\n{exec_results[2]}')
            break
        print(f'Тест №{file_name}: {Fore.GREEN}passed{Fore.WHITE}')
    tests_files.close()


def open_file_in_zip(tests_files, file_name):
    answer_filename = '{}.clue'.format(file_name)
    return read_decode(tests_files, file_name),\
        read_decode(tests_files, answer_filename)


def read_decode(tests_files, file_name):
    return tests_files.open(file_name).read().decode('utf-8')
