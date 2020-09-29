import datetime
import logging
import functools


def log_message(logger, message, level=logging.INFO):
    """Helper to log a message using a given logger

    Args:
        logger (logger): logger to log with
        message (string): message to log
        level (logging.level, optional): logging level to use. Defaults to logging.INFO.
    """
    logger.log(level=level, msg=message)


def log(logger, level=logging.DEBUG):
    """logger factory, recieves logger to use and returns function decorator

    Args:
        logger (logging.logger): logger to use
    """

    def decorator(func):
        """
        Function decorator to log calls.
        Logs datetime, function name, and parameters.

        Args:
            func (Callable): Function to be logged
        Returns:
            Callable: Wrapped function with logging
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            msg = f"{logger.__module__}: {func.__name__} ({repr(args)}, {repr(kwargs)})"
            logger.log(level=level, msg=msg)
            return func(*args, **kwargs)

        return wrapper
    return decorator

# def logged(func):
#     """
#     Function decorator to log calls.
#     Logs datetime, function name, and parameters.

#     Args:
#         func (Callable): Function to be logged
#      Returns:
#         Callable: Wrapped function with logging
#     """
#     # Wrapped call to func with logging
#     logger = logging.getLogger(func.__module__)

#     def logged_wrapper(*args, **kwargs):

#         msg = f"{func.__name__} ({str(args)}, {str(kwargs)})"
#         logger.info(msg)
#         return func(*args, **kwargs)

#     return logged_wrapper
