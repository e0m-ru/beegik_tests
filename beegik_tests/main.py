from .helpers import *


def run_one_test(test: str, answer: str) -> bool:
    """выполняет один тестовый случай, 
    сравнивая полученный результат с ожидаемым ответом."""
    result = capture_output(test)
    return answer == result.strip()


def run(test_zip_file: str | int, context: dict, verbose=None):
    """принимает два аргумента:\n
    test_zip_file - имя zip файла с тестами\n
    context - контекст выполнения (globals() например)
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
