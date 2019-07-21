class BaseDescriptor:
    """
    Base descriptor class to set a value
    """

    def __init__(self, **opts):
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Condition:
    def __init__(self, method, inner_exception=TypeError, msg=""):
        self._method = method
        self._inner_exception = inner_exception
        self._msg = msg

    def holds(self, value):
        if not self._method(value):
            raise self._inner_exception(self._msg)
        return True


def Constrained(condition, cls=None):
    if cls is None:
        return lambda cls: Constrained(condition, cls)

    super_set = cls.__set__

    def __set__(self, instance, value):
        if condition.holds(value):
            super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# Usage example:
@Constrained(Condition(method=lambda x: isinstance(x, int)))
class Integer(BaseDescriptor):
    pass


class Stock:
    shares = Integer()

    def __init__(self, shares):
        self.shares = shares
