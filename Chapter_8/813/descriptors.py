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


class Typed(BaseDescriptor):
    """
    This descriptor will enforce 'expected_type' type to value
    """

    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Type {self.expected_type} expected")
        super().__set__(instance, value)


class Unsigned(BaseDescriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Value >= 0 expected.")
        super().__set__(instance, value)


class MaxSized(BaseDescriptor):
    """
    This descriptor implements the maximum length (strlen) for a value
    """

    def __init__(self, **opts):
        if "size" not in opts:
            raise AttributeError('Expected "size" option.')
        super().__init__(**opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError(f"The size of the value must be < {self.size}")
        super().__set__(instance, value)


# The descriptors below implement different typed constrants, and as well
# some other properties with Mixins.


class Integer(Typed):
    expected_type = int


class UnsignedInt(Integer, Unsigned):
    pass


class Float(Typed):
    expected_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    expected_type = str


class SizedString(String, MaxSized):
    pass


# Approach 1.
# Finally, we implement a target data structure
class Stock:
    tag = SizedString(size=5)
    shares = UnsignedInt()
    price = UnsignedFloat()

    def __init__(self, tag, shares, price):
        self.tag = tag
        self.shares = shares
        self.price = price


# Approach 2.
# An alternative approach is to use a class decorator
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, BaseDescriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls

    return decorate


# And an example of how this is used:
@check_attributes(tag=SizedString(size=5), shares=UnsignedInt(), price=UnsignedFloat())
class NewStock:
    def __init__(self, tag, shares, price):
        self.tag = tag
        self.shares = shares
        self.price = price


# Approach 3.
# Using metaclass
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        # Attach attribute names to the descriptors
        for key, value in methods.items():
            if isinstance(value, BaseDescriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


# And an example of how this is used:
class frommetaStock(metaclass=checkedmeta):
    tag = SizedString(size=5)
    shares = UnsignedInt()
    price = UnsignedFloat()

    def __init__(self, tag, shares, price):
        self.tag = tag
        self.shares = shares
        self.price = price


# Small comments:
# As you can see, there is no difference between the Stock and the formmetaStock classes implementation,
# except the metaclass=checkedmeta part. This is because in the book they didn't implement __set_name__
# in the original descriptor.
