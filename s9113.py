from collections import UserDict
import beegik_tests as beegik_tests


class MultiKeyDict(UserDict):
    def __init__(self, *args, **kwargs):
        self._alias = dict()
        super().__init__(self, *args, **kwargs)

    def alias(self, key, alias):
        self._alias[key] = key
        self._alias[alias] = key

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self._alias:
            key = self._alias[key]
            return self.data[key]
        elif (key not in self._alias) and (key in self.data):
            raise KeyError(key)
        elif (key in self.data):
            return self.data[key]

    def __setitem__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        elif key in self.data:
            self.data[key] = value
        elif key in self._alias:
            self.data[self._alias[key]] = value
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if key in self._alias:
            self.data[key] = self.data[self._alias[key]]
            self._alias[self._alias[key]] = key
            del self._alias[key]
            # del self.data[key]


tests = beegik_tests.Test_manager(
    '13.zip', globals())
tests.run()
