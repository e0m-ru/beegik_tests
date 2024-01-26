import beegeek_tests.beegeek_tests as beegik_tests


from collections import UserDict

class MultiKeyDict(UserDict):
    def __init__(s, *a, **k): s._a = {}; super().__init__(*a, **k)
    def alias(s, k, a): s._a[a] = k

    def __getitem__(s, k):
        if k in s.data and k in s._a:
            return s.data[k]
        return s.data[s._a[k]]

    def __setitem__(s, k, v):
        if k in s._a:
            k = s._a[k]
        s.data[k], s._a[k] = v, k

    def __delitem__(s, k):
        if s._a.get(k) == k:
            s._a.pop(k)
        if k in s.data and not any(v == k for v in s._a.values()):
            s.data.pop(k)


tests = beegik_tests.Test_manager(
    '13.zip', globals())
tests.run()
