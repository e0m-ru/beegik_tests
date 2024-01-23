from collections import UserDict
import beegik_tests as beegik_tests


class MultiKeyDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._alias = dict()

    def alias(self, key, alias):
        self._alias[alias] = key

    def __getitem__(self, key):
        if key in self:
            key = self._alias[key]
        return self.data[key]

    def __setitem__(self, key, value):
        # key = self._alias[key]
        if '_alias' in self.__dict__:
            key = self.__dict__['_alias'].__get__(key, key)
        self.data[key] = value


tests = beegik_tests.Test_manager(
    '13.zip', globals())
# tests.run()

multikeydict = MultiKeyDict(x=100)

multikeydict.alias('x', 'z')
del multikeydict['x']
print(multikeydict['z'])

try:
    print(multikeydict['x'])
except KeyError:
    print('Ключ отстутствует')
