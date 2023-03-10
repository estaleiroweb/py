import math


class MainOperations:
    def __init__(self) -> None:
        self._start_init()
        self.value = None
        self._end_init()

    def _start_init(self):
        self.__dict__['_init'] = True

    def _end_init(self):
        self.__dict__['_init'] = False

    def conv2Num(self, n) -> 'int|float':
        return n if isinstance(n, int) or isinstance(n, float) else float(n)


class MathOperations(MainOperations):
    def __add__(self, other): return self.value + self.conv2Num(other)
    def __sub__(self, other): return self.value - self.conv2Num(other)
    def __mul__(self, other): return self.value * self.conv2Num(other)
    def __floordiv__(self, other): return self.value // self.conv2Num(other)
    def __truediv__(self, other): return self.value / self.conv2Num(other)
    def __mod__(self, other): return self.value % self.conv2Num(other)
    def __pow__(self, other): return self.value ** self.conv2Num(other)
    def __divmod__(self, other): return self.value / \
        self.conv2Num(other)  # check if works

    def __iadd__(self, other): self.value += self.conv2Num(other)
    def __isub__(self, other): self.value -= self.conv2Num(other)
    def __imul__(self, other): self.value *= self.conv2Num(other)
    def __ifloordiv__(self, other): self.value //= self.conv2Num(other)
    def __itruediv__(self, other): self.value /= self.conv2Num(other)
    def __idiv__(self, other): self.value /= self.conv2Num(other)
    def __imod__(self, other): self.value %= self.conv2Num(other)
    def __ipow__(self, other): self.value **= self.conv2Num(other)

    # check if works
    def __rfloordiv__(self, other): return self.value // self.conv2Num(other)

    def __radd__(self, other): return self.value + \
        self.conv2Num(other)  # check if works

    def __rsub__(self, other): return self.value - \
        self.conv2Num(other)  # check if works

    def __rmul__(self, other): return self.value * \
        self.conv2Num(other)  # check if works
    def __rmod__(self, other): return self.value % self.conv2Num(
        other)  # check if works
    # check if works
    def __rpow__(self, other): return self.value ** self.conv2Num(other)

    def __rtruediv__(self, other): return self.value / \
        self.conv2Num(other)  # check if works
    def __rdivmod__(self, other): return self.value / \
        self.conv2Num(other)  # check if works


class FunctionOperations(MainOperations):
    def __pos__(self): return abs(self.value)
    def __neg__(self): return abs(self.value) * -1
    def __abs__(self): return abs(self.value)
    def __ceil__(self): return math.ceil(self.value)
    def __floor__(self): return math.floor(self.value)
    def __trunc__(self): return math.trunc(self.value)
    def __round__(self, n): return round(self.value, n)
    def __nonzero__(self): return self.value != None and self.value != 0
    def __dir__(self): return dir(self.value)
    def __sizeof__(self): return self.value.__sizeof__  # sys.getsizeof()


class LogicOperations(MainOperations):
    def __eq__(self, other): return self.value == other
    def __ne__(self, other): return self.value != other
    def __lt__(self, other): return self.value < other
    def __le__(self, other): return self.value <= other
    def __gt__(self, other): return self.value > other
    def __ge__(self, other): return self.value >= other
    def __and__(self, other): return self.value and other
    def __or__(self, other): return self.value or other
    def __bool__(self): return bool(self.value)


class BinaryOperations(MainOperations):
    def __invert__(self): return ~self.value
    def __xor__(self, other): return self.value ^ other  # check if works
    def __lshift__(self, other): return self.value << other
    def __rshift__(self, other): return self.value >> other  # check if works

    def __rlshift__(self, other): return ~(
        ~self.value << other)  # check if works
    def __rrshift__(self, other): return ~(
        ~self.value >> other)  # check if works

    def __ilshift__(self, other): self.value <<= other
    def __irshift__(self, other): self.value >>= other
    def __iand__(self, other): self.value &= other
    def __ior__(self, other): self.value |= other
    def __ixor__(self, other): self.value ^= other

    def __rxor__(self, other): return other ^ self.value  # check if works
    def __ror__(self, other): return other | self.value  # check if works
    def __rand__(self, other): return other & self.value  # check if works


class StringOperations(MainOperations):
    def __str__(self): return f'{self.value}'  # Invoked with print()
    def __repr__(self): return repr(self.value)
    def __format__(self, formatstr): return str(self.value).format(formatstr)
    def __hash__(self): return hash(self.value)
    # def __unicode__(self): return unicode(self.value)


class CastOperations(MainOperations):
    def __int__(self): return int(self.value)
    def __float__(self): return float(self.value)
    def __complex__(self): return complex(self.value)
    def __oct__(self): return oct(self.value)
    def __hex__(self): return hex(self.value)
    # def __index__(self): return int(self.value) #To get called on type conversion to an int when the object is used in a slice expression.


class AttributeOperations(MainOperations):
    def __setattr__(self, name, value):
        try:
            getattr(self, '_set_'+name)(value)
        except:
            if self.__dict__.get('_init', False) or name in self.__dict__.keys():
                self.__dict__[name] = value

    # def __getattr__(self, name):
    #     ...

    # def __delattr__(self, name):
    #     ...


class AllOperations(AttributeOperations, CastOperations, StringOperations, BinaryOperations, LogicOperations, FunctionOperations, MathOperations):
    ...
