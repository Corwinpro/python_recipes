"""
This approach is proposed as an alternative, which uses class decorators
"""


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


# This provides type checking for descriptor
# I will explain how it works inside the code, along the way
def Typed(expected_type, cls=None):
    # This first case appears straight away after the definition of the decorator.
    # We would type somthing like: `Typed(int)`, and therefore `cls is None`.
    if cls is None:
        # We return a lambda function with the expected type built-in.
        return lambda cls: Typed(expected_type, cls)

    # Otherwise, we will reload the __set__ of the decorated class.
    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# Usage example:
@Typed(int)
class Integer(BaseDescriptor):
    pass


# This decorator takes no arguments
def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls
