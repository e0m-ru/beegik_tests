"""Реализуйте класс MultiKeyDict, 
который практически во всем повторяет класс dict. 
Создание экземпляра класса MultiKeyDict 
должно происходить аналогично созданию экземпляра класса dict:
>>> multikeydict1 = MultiKeyDict(x=1, y=2, z=3)
>>> multikeydict2 = MultiKeyDict([('x', 1), ('y', 2), ('z', 3)])
>>> print(multikeydict1['x'])
1
>>> print(multikeydict2['z'])
3

Особенностью класса MultiKeyDict должен являться метод alias(),
который должен позволять давать имеющимся ключам псевдонимы.
Обращение по созданному псевдониму не должно ничем отличаться 
от обращения по оригинальному ключу, то есть с момента создания псевдонима 
у значения становится два ключа (или больше, если псевдонимов несколько):
>>> multikeydict = MultiKeyDict(x=100, y=[10, 20])
>>> multikeydict.alias('x', 'z')     # добавление ключу 'x' псевдонима 'z'
>>> multikeydict.alias('x', 't')     # добавление ключу 'x' псевдонима 't'
>>> print(multikeydict['z'])
100
>>> multikeydict['t'] += 1
>>> print(multikeydict['x'])
101
>>> multikeydict.alias('y', 'z')     # теперь 'z' становится псевдонимом ключа 'y'
>>> multikeydict['z'] += [30]
>>> print(multikeydict['y'])
[10, 20, 30]

Значение должно оставаться доступным по псевдониму даже в том случае, если оригинальный ключ был удален:
>>> multikeydict = MultiKeyDict(x=100)
>>> multikeydict.alias('x', 'z')
>>> del multikeydict['x']
>>> print(multikeydict['z'])
100

Ключи должны иметь приоритет над псевдонимами. 
Если некоторые ключ и псевдоним совпадают, 
то все операции при обращении к ним должны выполняться именно с ключом:
>>> multikeydict = MultiKeyDict(x=100, y=[10, 20])
>>> multikeydict.alias('x', 'y')
>>> print(multikeydict['y'])
[10, 20]"""
# if __name__ == '__main__':
#     import doctest
#     doctest.testmod(verbose=False)

from collections import UserDict
import beegik_tests as beegik_tests


class MultiKeyDict(UserDict):
    def __init__(self, *args, **kwargs):
        self._aliases = {}
        super().__init__(*args, **kwargs)

    def alias(self, original_key, alias_key):
        self._aliases[alias_key] = original_key
        self._aliases[original_key] = original_key

    def __getitem__(self, key):
        if (key in self._aliases) and (key in self.data):
            return super().__getitem__(key)
        if (key in self._aliases) and (key not in self.data):
            key = self._aliases[key]
            return super().__getitem__(key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        if key in self._aliases:
            key = self._aliases[key]
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if (key in self._aliases) and (key in self.data):
            del self.data[key]
        elif (key in self._aliases) and (key not in self.data):
            del self._aliases[key]


tests = beegik_tests.Test_manager(
    '13.zip', globals())
tests.run()

multikeydict = MultiKeyDict(x=100)

multikeydict.alias('x', 'z')
del multikeydict['x']
print(multikeydict.__dict__)
# print(multikeydict['z'])

try:
    print(multikeydict['x'])
except KeyError:
    print('Ключ отстутствует')
