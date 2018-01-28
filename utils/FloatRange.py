
class FloatRange:
    def __init__(self, start, stop, step, precision=8):
        self.value = start
        self.stop = stop
        self.step = step
        self.precision = precision

    def __iter__(self):
        return self

    def __next__(self):
        value = self.value
        if self.step > 0 and value >= self.stop:
            raise StopIteration()
        if self.step < 0 and value <= self.stop:
            raise StopIteration()

        self.value = round(self.value + self.step, self.precision)
        return value


if __name__ == "__main__":
    n = 1000
    for i, epsilon in enumerate([1.0 - k / n for k in range(n + 1)]):
        print(i, epsilon)

    for i, epsilon in enumerate(FloatRange(1.0, 0.0, -1/n)):
        print(i, epsilon)
