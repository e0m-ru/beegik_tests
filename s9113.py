from collections import UserDict
import beegik_tests as beegik_tests


class MultiKeyDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._alias = dict()

    def alias(self, key, alias):
        self._alias.update({alias: key})

    def __getitem__(self, key):
        key = self.__dict__['_alias'].get(key, key)
        return self.data.get(key)

    def __setitem__(self, key, value):
        print(self.__getattribute__('alias'))
        self.data.update({key: value})


tests = beegik_tests.Test_manager(
    '13.zip', globals())
# tests.run()
multikeydict = MultiKeyDict(x=100, y=[10, 20])

multikeydict.alias('x', 'z')
multikeydict.alias('x', 't')
print(multikeydict['z'])
multikeydict['t'] += 1
# print(multikeydict['x'])
# multikeydict.alias('y', 'z')
# multikeydict['z'] += [30]
# print(multikeydict['y'])
print(multikeydict.__dict__)
