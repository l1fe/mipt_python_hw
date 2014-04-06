__author__ = 'inaumov'

def logging(func, log_file):
    def wrap(*args, **kwargs):
        res = func(*args, **kwargs)
        import logging
        logging.basicConfig(filename = log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info((func.__name__, args, kwargs))

        return res

    return wrap