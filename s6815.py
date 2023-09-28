import beegik_tests

# https://stepik.org/lesson/810856/step/16?auth=login&unit=816647

# решение


class NonNegativeInteger:
    def __init__(self, name, default=None) -> None:
        self.name = name
        self.default = default

    def __set__(self, obj, value):
        if isinstance(value, int) and value >= 0:
            obj.__dict__[self.name] = value
        else:
            raise ValueError('Некорректное значение')

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.name in obj.__dict__:
            return obj.__dict__[self.name]
        elif self.default is not None:
            return self.default
        else:
            raise AttributeError('Атрибут не найден')


# запуск тестов из архива 16
tests = beegik_tests.Test_manager(
    '16.zip', {'NonNegativeInteger': NonNegativeInteger})
tests.run()
