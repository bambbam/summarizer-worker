from typing import Union
import functools
import logging

from torch import is_inference

class MyLogger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename="log.txt")
        
    def get_logger(self, name=None):
        return logging.getLogger(name)

def get_default_logger():
    return MyLogger().get_logger()


def log(my_logger: Union[MyLogger, logging.Logger] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(func, my_logger)
            logger = None
            if my_logger is None:
                logger = get_default_logger()
            elif isinstance(my_logger, MyLogger):
                logger = my_logger.get_logger(func.__name__)
            else:
                logger = my_logger
            
            args_repr = [repr(arg) for arg in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(f"function {func.__name__} called with args {signature}")
            
            try:
                result = func(*args, **kwargs);
                return result
            except Exception as e:  
                logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
                raise e        
        return wrapper
    return decorator