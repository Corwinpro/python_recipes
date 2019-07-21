This example deals with different *descriptors* techniques, as a way to implement constrained attributes.

The approach with class decorators runs much faster (according to the book).

My comments:

It seems to be more versatile if we defined a `Condition` class instead of repeating the code and applying the reusing `__set__` implementation with different conditions on the values.

Also, why not use pre and post contracts?