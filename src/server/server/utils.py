import datetime
import os

def logged(func):
    """
    Function decorator to log calls.
    Logs datetime, function name, and parameters.

    Args:
        func (Callable): Function to be logged
     Returns:
        Callable: Wrapped function with logging
    """
    # Wrapped call to func with logging
    def logged_wrapper(*args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log function call
        print(f"log {date}: {func.__name__} called with {str(args)}")

        # Call function with original parameters
        return func(*args, **kwargs)
    return logged_wrapper

import logging
logger = logging.getLogger("test")
logger.debug("logged")