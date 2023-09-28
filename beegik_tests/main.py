from .helpers import *
import zipfile
from colorama import Fore


def run_one_test(test: str, answer: str, context) -> bool:
    """выполняет один тестовый случай, 
    возвращает полученный результат и ожидаемый ответ."""
    result = capture_output(test, context)
    return answer == result, result, answer


def run(test_zip_file: str | int, context: dict):
    """принимает два аргумента:\n
    test_zip_file - имя zip файла с тестами\n
    context - контекст выполнения (globals() например)
    """
    zip_file = zipfile.ZipFile(f'{test_zip_file}.zip')

    for file_name in zip_file.namelist()[::2]:
        passed = run_one_test(*open_file_in_zip(zip_file, file_name), context)
        if passed[0] is False:
            test_number = file_name
            print(
                f'{Fore.RED}Failed on test № {file_name}{Fore.WHITE}\nresult:\n{passed[1]}\nanswer:\n{passed[2]}')
            break
        print(f'Тест №{file_name}: {Fore.GREEN}passed{Fore.WHITE}')
    zip_file.close()


def open_file_in_zip(zip_file, file_name):
    answer_filename = '{}.clue'.format(file_name)
    return read_decode(zip_file, file_name),\
        read_decode(zip_file, answer_filename)


def read_decode(zip_file, file_name):
    return zip_file.open(file_name).read().decode('utf-8')
