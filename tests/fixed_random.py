import functools
import random


def fixed_random(seed: int = 0):
    """Temporarily sets the random RNG to a seeded state, executes func, then returns state to original."""
    def decorator_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            state = random.getstate()
            random.seed(seed)
            func(*args, **kwargs)
            random.setstate(state)
        return wrapper
    return decorator_wrapper
