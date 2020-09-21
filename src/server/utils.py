import datetime

def logged(func):
    def logged_wrapper(*args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"log {date}: {func.__name__} called with {str(args)}")
        return func(*args, **kwargs)
    return logged_wrapper