import sys
from pprint import pprint
import random


class foo:
    @property
    def v1(self):
        print(sys._getframe().f_code.co_filename)
        print(sys._getframe().f_code.co_name)
        print(sys._getframe().f_code.co_argcount)
        print(sys._getframe().f_code.co_firstlineno)
        print(sys._getframe().f_code.co_varnames)
        # print(sys._getframe().f_code.co_flags)
        print(sys._getframe().f_lineno)

        return self.__dict__.get('v1', 123)


# f=foo()
# print(f.v1)

def tst(*args, **kargs):
    print(args)
    print(kargs)

# tst(eu=123)
# tst(123)


class Iter:
    # def __new__(cls):
    #     return iter(object.__new__(cls))
    
    def __init__(self, lst: list):
        self._collection = lst
        self._pos = 0
        self._len = len(lst)

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < self._len:
            self._pos += 1
            return self._collection[self._pos-1]
        else:
            raise StopIteration




i=Iter([1, 3, 5, 7, 9])

print(i)
print(next(i))
print(next(i))
print(next(i))
print(next(i))
print(next(i))
print(next(i,222))


k = ( 'a', 'b', 'c')
v = ( 1, 2, 3 )
v = [( 1, 2, 3 ),( 1, 2, 3 )]

r=dict(zip(k,v))
r2 = [dict(zip(k,i)) for i in v]

pprint(r)
pprint(r2)
