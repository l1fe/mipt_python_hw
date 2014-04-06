__author__ = 'inaumov'

def decorator(func):
    import time

    def wrap(*args, **kwargs):
        start_time = time.clock()

        result_func = func(*args, **kwargs)

        print(time.clock() - start_time)

        return result_func

    return wrap