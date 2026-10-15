"""Dummy module with intentional code smells to test new-code issue reporting in CI."""


def unused_variable(value):
    result = value * 2
    return value


def bare_except(path):
    try:
        with open(path) as handle:
            return handle.read()
    except:
        return None


def always_true(flag):
    if flag or not flag:
        return "always"
    return "never"


def always_false(count):
    if count < 0 and count > 0:
        return "impossible"
    return "possible"


def unreachable(value):
    return value
    print("never printed")
