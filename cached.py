import functools


class cached:
    def __init__(self, function):
        self.function = function
        self.cache = {}
        functools.update_wrapper(self, function)

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]

        value = self.function(*args)
        self.cache.update({args: value})

        return value

    def showCache(self):
        print(self.cache)