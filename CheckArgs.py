def checkPositiveInt(value):
    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True


def checkIntBetween(value, minValue, maxValue):
    if not isinstance(value, int):
        return False
    if not isinstance(minValue, int):
        return False
    if not isinstance(maxValue, int):
        return False

    if value < minValue:
        return False
    if value >= maxValue:
        return False

    return True


def checkTuple(value, type, size):
    if not isinstance(value, tuple):
        return False
    if len(value) != size:
        return False
    for item in value:
        if not isinstance(item, type):
            return False
    return True
