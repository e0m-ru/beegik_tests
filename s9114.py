class predicate:
    def __init__(s,f):s.f=f
    def __call__(s,*a,**k):return s.f(*a,**k)
    def __and__(s,o):return lambda *a,**k:s(*a,**k)&o(*a,**k)
    def __or__(s,o):return lambda *a,**k:s(*a,**k)|o(*a,**k)
    def __invert__(s):return predicate(lambda *a,**k:not s.f(*a,**k))

from beegeek_tests.beegeek_tests import Test_manager as test
test('14.zip',globals()).run(
    # _verbose=True,
    # _code=True,
    # number=1,
    )
